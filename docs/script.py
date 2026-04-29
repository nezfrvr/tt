import random


days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
grades = ['G4', 'G5', 'G6', 'G7', 'G8']
period_count = {'G4': 8, 'G5': 8, 'G6': 9, 'G7': 9, 'G8': 9}
teacher_codes = {'Pauline': 1, 'Patience': 7, 'Mumo': 4, 'Steve': 2, 'Josphat': 3, 'Joyce': 5}

allocations = {
    'Pauline': {
        'G4': {'Kiswahili': 4, 'CRE': 3, 'Nutrition': 2},
        'G5': {'Kiswahili': 4, 'CRE': 3, 'Nutrition': 2},
        'G6': {'CRE': 3, 'Nutrition': 2},
        'G7': {'Nutrition': 2},
        'G8': {'Nutrition': 2},
    },
    'Patience': {
        'G4': {'Kiswahili': 4, 'SStudies': 4, 'Math': 5},
        'G5': {'SStudies': 4},
        'G7': {'Kiswahili': 4, 'SStudies': 4},
        'G8': {'Kiswahili': 4, 'SStudies': 4},
    },
    'Mumo': {
        'G4': {'Science': 5},
        'G5': {'Science': 5},
        'G6': {'Math': 5, 'Science': 5},
        'G7': {'Math': 5, 'Business': 2},
        'G8': {'Business': 2},
    },
    'Steve': {
        'G4': {'Creative Arts': 6},
        'G5': {'Creative Arts': 6},
        'G6': {'Creative Arts': 6, 'Sstudies': 4},
        'G7': {'Creative Arts': 6},
        'G8': {'Creative Arts': 6},
    },
    'Josphat': {
        'G4': {'Agriculture': 2},
        'G5': {'Math': 5, 'Agriculture': 2},
        'G6': {'Agriculture': 2},
        'G7': {'Science': 5, 'Pre tech': 2, 'Agriculture': 2},
        'G8': {'Math': 5, 'Science': 5, 'Pre tech': 2, 'Agriculture': 2},
    },
    'Joyce': {
        'G4': {'English': 5},
        'G5': {'English': 5},
        'G6': {'English': 5},
        'G7': {'English': 5, 'CRE': 4},
        'G8': {'English': 5, 'CRE': 4},
    },
}

period_times = {
    1: '08:10-08:50',
    2: '08:50-09:30',
    3: '09:30-10:10',
    4: '10:10-10:50',
    5: '11:00-11:40',
    6: '11:40-12:20',
    7: '12:20-13:00',
    8: '14:00-14:40',
    9: '14:40-15:20',
}


def build_requests():
    requests = []
    for teacher, grade_data in allocations.items():
        total = sum(sum(subjects.values()) for subjects in grade_data.values())
        for grade, subjects in grade_data.items():
            for subject, count in subjects.items():
                for _ in range(count):
                    requests.append({
                        'teacher': teacher,
                        'grade': grade,
                        'subject': subject,
                        'count': count,
                        'total': total,
                    })
    requests.sort(key=lambda r: (
        r['teacher'] != 'Joyce',
        -r['count'],
        -r['total'],
        r['grade'],
        r['subject'],
    ))
    return requests


def build_empty_schedule():
    return {
        grade: {day: {p: None for p in range(1, period_count[grade] + 1)} for day in days}
        for grade in grades
    }


def build_teacher_schedule():
    return {
        teacher: {day: {} for day in days}
        for teacher in teacher_codes
    }


def can_assign(grade_schedule, teacher_schedule, teacher, grade, day, period):
    if grade_schedule[grade][day][period] is not None:
        return False
    if period in teacher_schedule[teacher][day]:
        return False
    previous = teacher_schedule[teacher][day].get(period - 1)
    if previous is not None and previous != grade:
        return False
    next_period = teacher_schedule[teacher][day].get(period + 1)
    if next_period is not None and next_period != grade:
        return False
    return True


def find_valid_slots(grade_schedule, teacher_schedule, teacher, grade):
    slots = []
    for day in days:
        for period in range(1, period_count[grade] + 1):
            if can_assign(grade_schedule, teacher_schedule, teacher, grade, day, period):
                day_load = len(teacher_schedule[teacher][day])
                slots.append((day_load, period, day))
    return slots


def schedule_lessons():
    grade_schedule = build_empty_schedule()
    teacher_schedule = build_teacher_schedule()
    requests = build_requests()

    while requests:
        options = []
        for idx, req in enumerate(requests):
            valid_slots = find_valid_slots(grade_schedule, teacher_schedule, req['teacher'], req['grade'])
            if not valid_slots:
                return None
            options.append((len(valid_slots), req['total'], req['count'], random.random(), idx, valid_slots))

        options.sort()
        _, _, _, _, chosen_index, valid_slots = options[0]
        req = requests.pop(chosen_index)

        valid_slots.sort(key=lambda slot: (slot[0], slot[1], slot[2], random.random()))
        _, period, day = valid_slots[0]

        grade_schedule[req['grade']][day][period] = (req['subject'], req['teacher'])
        teacher_schedule[req['teacher']][day][period] = req['grade']

    return grade_schedule, teacher_schedule


schedule = None
for attempt in range(1, 101):
    result = schedule_lessons()
    if result is not None:
        schedule = result
        break
    random.shuffle(days)

if schedule is None:
    raise RuntimeError('Unable to build a valid timetable after multiple attempts.')


grade_schedule, teacher_schedule = schedule

html = ['<!DOCTYPE html>', '<html>', '<head>',
        '<meta charset="utf-8">',
        '<title>Beach Academy Timetable</title>',
        '<style>',
        'body { font-family: Arial, sans-serif; margin: 20px; background: #f5f7fb; color: #1f2937; }',
        'h1, h2, h3 { margin: 20px 0 10px; }',
        'table { width: 100%; border-collapse: collapse; margin-bottom: 32px; }',
        'th, td { border: 1px solid #cbd5e1; padding: 8px; text-align: center; }',
        'th { background: #0f172a; color: white; }',
        '.day-table th { background: #0ea5e9; }',
        '.teacher-table th { background: #16a34a; }',
        '.small { font-size: 0.85rem; color: #475569; }',
        '.subject { font-weight: 700; }',
        '.code { color: #2563eb; }',
        '.section { background: white; padding: 16px; border-radius: 10px; box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08); }',
        '</style>',
        '</head>',
        '<body>',
        '<div class="section"><h1>Beach Academy Weekly Timetable</h1>',
        '<p class="small">Period times are shown for orientation. Teacher code labels are included beside each subject.</p>',
]

for day in days:
    html.append(f'<div class="section"><h2>{day}</h2><table class="day-table">')
    html.append('<tr><th>Period</th><th>Time</th>' + ''.join(f'<th>{grade}</th>' for grade in grades) + '</tr>')
    max_period = max(period_count.values())
    for period in range(1, max_period + 1):
        html.append('<tr>')
        html.append(f'<td>{period}</td>')
        html.append(f'<td>{period_times.get(period, "")}</td>')
        for grade in grades:
            if period <= period_count[grade]:
                entry = grade_schedule[grade][day][period]
                if entry:
                    subject, teacher = entry
                    code = teacher_codes[teacher]
                    html.append(f'<td><span class="subject">{subject}</span> <span class="code">({code})</span></td>')
                else:
                    html.append('<td>Free</td>')
            else:
                html.append('<td style="background:#e2e8f0;">N/A</td>')
        html.append('</tr>')
    html.append('</table></div>')

html.append('<div class="section"><h2>Individual teacher timetables</h2>')
for teacher in sorted(teacher_codes.keys()):
    html.append(f'<div><h3>{teacher} ({teacher_codes[teacher]})</h3>')
    html.append('<table class="teacher-table">')
    html.append('<tr><th>Period</th><th>Time</th>' + ''.join(f'<th>{day}</th>' for day in days) + '</tr>')
    max_period = max(period_count.values())
    for period in range(1, max_period + 1):
        html.append('<tr>')
        html.append(f'<td>{period}</td>')
        html.append(f'<td>{period_times.get(period, "")}</td>')
        for day in days:
            subject_text = ''
            grade = teacher_schedule[teacher][day].get(period)
            if grade:
                subject = grade_schedule[grade][day][period][0]
                subject_text = f'{grade} - {subject} ({teacher_codes[teacher]})'
            html.append(f'<td>{subject_text}</td>')
        html.append('</tr>')
    html.append('</table></div>')
html.append('</div></body></html>')

with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(html))

import random

grades = ['G4', 'G5', 'G6', 'G7', 'G8']
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
teachers = ['Pauline', 'Patience', 'Mumo', 'Steve', 'Josphat', 'Joyce']
teacher_codes = {'Pauline':1, 'Patience':7, 'Mumo':4, 'Steve':2, 'Josphat':3, 'Joyce':5}

allocations = {
'Pauline': {
'G4': {'Kiswahili':4, 'CRE':3, 'Nutrition':2},
'G5': {'Kiswahili':4, 'CRE':3, 'Nutrition':2},
'G6': {'CRE':3, 'Nutrition':2},
'G7': {'Nutrition':2},
'G8': {'Nutrition':2}
},
'Patience': {
'G4': {'Kiswahili':4, 'SStudies':4, 'Math':5},
'G5': {'SStudies':4},
'G7': {'Kiswahili':4, 'SStudies':4},
'G8': {'Kiswahili':4, 'SStudies':4}
},
'Mumo': {
'G4': {'Science':5},
'G5': {'Science':5},
'G6': {'Math':5, 'Science':5},
'G7': {'Math':5, 'Business':2},
'G8': {'Business':2}
},
'Steve': {
'G4': {'Creative Arts':6},
'G5': {'Creative Arts':6},
'G6': {'Creative Arts':6, 'Sstudies':4},
'G7': {'Creative Arts':6},
'G8': {'Creative Arts':6}
},
'Josphat': {
'G4': {'Agriculture':2},
'G5': {'Math':5, 'Agriculture':2},
'G6': {'Agriculture':2},
'G7': {'Science':5, 'Pre tech':2, 'Agriculture':2},
'G8': {'Math':5, 'Science':5, 'Pre tech':2, 'Agriculture':2}
},
'Joyce': {
'G4': {'English':5},
'G5': {'English':5},
'G6': {'English':5},
'G7': {'English':5, 'CRE':4},
'G8': {'English':5, 'CRE':4}
}
}

slots = []
for grade in grades:
  max_p = 8 if grade in ['G4','G5'] else 9
  for day in days:
    for p in range(1, max_p+1):
      slots.append((day, p, grade))

used = set()
teacher_busy = {t: set() for t in teachers}
teacher_last_period = {t: {} for t in teachers}
assignments = {}

for teacher in teachers:
  for grade, subjects in allocations[teacher].items():
    for subject, count in subjects.items():
      for _ in range(count):
        available = [s for s in slots if s[2] == grade and s not in used and (s[0], s[1]) not in teacher_busy[teacher]]
        available = [s for s in available if not (s[0] in teacher_last_period[teacher] and abs(s[1] - teacher_last_period[teacher][s[0]]) == 1)]
        if available:
          slot = random.choice(available)
          used.add(slot)
          teacher_busy[teacher].add((slot[0], slot[1]))
          teacher_last_period[teacher][slot[0]] = slot[1]
          assignments[slot] = (subject, teacher_codes[teacher])
        else:
          print(f"No available slot for {teacher} {grade} {subject}")

timetable = {day: {grade: {} for grade in grades} for day in days}
for slot in slots:
  day, p, grade = slot
  if slot in assignments:
    subj, code = assignments[slot]
    timetable[day][grade][p] = f"{subj} ({code})"
  else:
    timetable[day][grade][p] = "Free"

html = """
<!DOCTYPE html>
<html>
<head>
<title>Beach Academy Timetable</title>
<style>
table { border-collapse: collapse; }
th, td { border: 1px solid black; padding: 5px; }
</style>
</head>
<body>
<h1>Beach Academy Timetable</h1>
"""

for day in days:
  html += f"<h2>{day}</h2>"
  html += "<table>"
  html += "<tr><th>Period</th>"
  for grade in grades:
    html += f"<th>{grade}</th>"
  html += "</tr>"
  max_p = 9
  for p in range(1, max_p+1):
    html += f"<tr><td>{p}</td>"
    for grade in grades:
      if p in timetable[day][grade]:
        html += f"<td>{timetable[day][grade][p]}</td>"
      else:
        html += "<td></td>"
    html += "</tr>"
  html += "</table>"

html += """
<h1>Teachers' Classes</h1>
"""

for teacher in teachers:
  html += f"<h2>{teacher} ({teacher_codes[teacher]})</h2>"
  html += "<table>"
  html += "<tr><th>Day</th><th>Period</th><th>Grade</th><th>Subject</th></tr>"
  for slot, (subj, code) in assignments.items():
    if code == teacher_codes[teacher]:
      day, p, grade = slot
      html += f"<tr><td>{day}</td><td>{p}</td><td>{grade}</td><td>{subj}</td></tr>"
  html += "</table>"

html += """
</body>
</html>
"""

print(html)
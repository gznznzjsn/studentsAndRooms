import json

from entities import student

with open("resources/students.json") as f:
    unparsed_students = json.load(f)

students = []
for i in range(0, len(unparsed_students)):
    students.append(student.Student(unparsed_students[i]["id"], unparsed_students[i]["name"],
                                    unparsed_students[i]["room"]))

for i in range(0, len(students)):
    print(students[i])

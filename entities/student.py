class Student:
    def __init__(self, student_id, name, room):
        self.id = student_id
        self.name = name
        self.room = room

    def __str__(self):
        return f"{self.id} {self.name} {self.room}"

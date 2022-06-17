import json
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey

from entities.models import Room, Student


class DBService(object):
    @staticmethod
    def get_student_list(filepath):
        with open(filepath) as input_file:
            strings = json.load(input_file)
        student_list = []
        for student in strings:
            student_list.append((student["birthday"], student["id"], student["name"],
                                 student["room"], student["sex"]))
        return student_list

    @staticmethod
    def get_extended_student_list_as_models(filepath):
        with open(filepath) as input_file:
            strings = json.load(input_file)
        student_list = []
        for student in strings:
            student_list.append(Student(birthday=student["birthday"], student_id=student["id"], name=student["name"],
                                        room_id=student["room"], sex=student["sex"]
                                        ))
        return student_list

    @staticmethod
    def get_room_list_as_models(filepath):
        with open(filepath) as input_file:
            strings = json.load(input_file)
        room_list = []
        for room in strings:
            room_list.append(Room(room_id=room["id"], name=room["name"]))
        return room_list

    @staticmethod
    def get_students_table(metadata):
        return Table("students", metadata,
                     Column('id', Integer(), primary_key=True),
                     Column('birthday', DateTime()),
                     Column('student_id', Integer),
                     Column('name', String(30)),
                     Column('room_id', ForeignKey("rooms.id")),
                     Column('sex', String(1))
                     )

    @staticmethod
    def get_rooms_table(metadata):
        return Table("rooms", metadata,
                     Column('id', Integer(), primary_key=True),
                     Column('room_id', Integer()),
                     Column('name', String(10))
                     )

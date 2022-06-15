import json
from entities.student import *
import xml.etree.ElementTree as ElementTree


class RoomService(object):
    @staticmethod
    def get_student_list(filepath):
        with open(filepath) as input_file:
            strings = json.load(input_file)
        student_list = []
        for student in strings:
            student_list.append(Student(student["id"], student["name"],
                                        student["room"]))
        return student_list

    @staticmethod
    def get_student_list_as_tuples(filepath):
        with open(filepath) as input_file:
            strings = json.load(input_file)
        student_list = []
        for student in strings:
            student_list.append((student["id"], student["name"],
                                 student["room"]
                                 ))
        return student_list

    @staticmethod
    def get_room_list_as_tuples(filepath):
        with open(filepath) as input_file:
            strings = json.load(input_file)
        room_list = []
        for room in strings:
            room_list.append((room["id"], room["name"]))
        return room_list

    @staticmethod
    def get_room_dictionary(filepath):
        with open(filepath) as input_file:
            strings = json.load(input_file)
        room_dictionary = {}
        for room in strings:
            room_dictionary[room["name"]] = {'id': room["id"],
                                             'students': []
                                             }
        return room_dictionary

    @staticmethod
    def fulfill_the_dorm(student_list, room_dictionary):
        for student in student_list:
            room_dictionary[f"Room #{student.room}"]['students'].append({'id': student.id,
                                                                         'name': student.name,
                                                                         'room': student.room
                                                                         })

    @staticmethod
    def save_as(format, room_dictionary):
        if str(format).upper() == "XML":

            dorm = ElementTree.Element('dorm')
            rooms = ElementTree.SubElement(dorm, 'rooms')
            for key in room_dictionary.keys():
                room = ElementTree.SubElement(rooms, "room")
                room.set("id", str(room_dictionary[key]['id']))
                room.set("name", str(key))
                for student in room_dictionary[key]['students']:
                    tmp_student = ElementTree.SubElement(room, "student")
                    tmp_student.set("id", str(student['id']))
                    tmp_student.set("name", student['name'])
                    tmp_student.set("room", str(student['room']))

            output_file = open("./resources/output/dorm.xml", "w")
            output_file.write(ElementTree.tostring(dorm).decode('utf-8'))

        else:
            if str(format).upper() == "JSON":

                with open('./resources/output/dorm.json', 'w') as output_file:
                    json.dump(room_dictionary, output_file)

            else:

                print("Wrong format!")

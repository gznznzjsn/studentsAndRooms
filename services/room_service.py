import json
import xml.etree.ElementTree as ElementTree


def get_student_list(filepath):
    with open(filepath) as input_file:
        strings = json.load(input_file)
    student_list = []
    for student in strings:
        student_list.append((student["id"], student["name"],
                             student["room"]))
    return student_list


def get_room_dictionary(filepath):
    with open(filepath) as input_file:
        strings = json.load(input_file)
    room_dictionary = {}
    for room in strings:
        room_dictionary[room["name"]] = {'id': room["id"],
                                         'students': []
                                         }
    return room_dictionary


def fulfill_the_dorm(student_list, room_dictionary):
    for student in student_list:
        room_dictionary[f"Room #{student[2]}"]['students'].append({'id': student[0],
                                                                   'name': student[1],
                                                                   'room': student[2]
                                                                   })


def save_as(output_format, room_dictionary):
    if str(output_format).upper() == "XML":
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

    if str(output_format).upper() == "JSON":
        with open('./resources/output/dorm.json', 'w') as output_file:
            json.dump(room_dictionary, output_file)

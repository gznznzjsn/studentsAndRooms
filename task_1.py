from services.room_service import *

students = input("Enter the path to students.json ")
student_list = RoomService.get_student_list(students)

rooms = input("Enter the path to rooms.json ")
room_dictionary = RoomService.get_room_dictionary(rooms)

RoomService.fulfill_the_dorm(student_list, room_dictionary)

format = input("Would you like to save as XML or JSON? ")
RoomService.save_as(format, room_dictionary)

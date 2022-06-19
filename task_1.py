from services.room_service import get_student_list, get_room_dictionary, fulfill_the_dorm, save_as

students = input("Enter the path to students.json ")
student_list = get_student_list(students)

rooms = input("Enter the path to rooms.json ")
room_dictionary = get_room_dictionary(rooms)

fulfill_the_dorm(student_list, room_dictionary)

output_format = input("Would you like to save as XML or JSON? ")
save_as(output_format, room_dictionary)

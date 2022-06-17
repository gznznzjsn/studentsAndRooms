from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.orm import sessionmaker

from entities.models import Room, Student
from services.db_service import DBService

engine = create_engine("mysql+mysqlconnector://root:1q2w3e@localhost/dorm")
metadata = MetaData()
factory = sessionmaker(bind=engine)
session = factory()

DBService.get_rooms_table(metadata)
DBService.get_students_table(metadata)
metadata.drop_all(engine)
metadata.create_all(engine)

session.add_all(DBService.get_room_list_as_models("./resources/input/rooms.json"))
session.commit()

for student in DBService.get_student_list("./resources/input/students_extended.json"):
    session.add(Student(birthday=student[0], student_id=student[1], name=student[2],
                        room_id=select(Room.id).where(Room.room_id == student[3]).scalar_subquery(),
                        sex=student[4]
                        ))
session.commit()

# for instance in session.query(Room):
#     print(instance.name, instance.id)

# try:
#     with connect(host="localhost", user=input("Username: "), password=getpass("Password: "),
#                  database=input("Database: ")) as connection:
#         create_db_query = "CREATE DATABASE dorm"
#         create_students_query = """CREATE TABLE students(
#                                 id INT AUTO_INCREMENT PRIMARY KEY,
#                                 student_id INT,
#                                 name VARCHAR(30),
#                                 room_id INT,
#                                 FOREIGN KEY(room_id) REFERENCES rooms(id)
#                                 )"""
#         create_rooms_query = """CREATE TABLE rooms(
#                                 id INT AUTO_INCREMENT PRIMARY KEY,
#                                 room_id INT,
#                                 name VARCHAR(30)
#                                 )"""
#         insert_students_query = """INSERT INTO students
#                                 (student_id,name, room_id)
#                                 VALUES(%s,%s,(SELECT id FROM rooms
#                                                 WHERE room_id = %s
#                                                 LIMIT 1
#                                                 ))"""
#         student_list = RoomService.get_extended_student_list_as_tuples("./resources/input/students.json")
#         insert_rooms_query = """INSERT INTO rooms
#                                 (room_id,name)
#                                 VALUES(%s,%s)"""
#         room_list = RoomService.get_room_list_as_tuples("./resources/input/rooms.json")
#         get_amount_in_rooms_query = """SELECT rooms.name, COUNT(student_id) AS amount
#                                         FROM students JOIN rooms ON students.room_id = rooms.id
#                                         GROUP BY rooms.room_id
#                                         ORDER BY rooms.room_id """
#         with connection.cursor() as cursor:
#             # cursor.execute(create_rooms_query)
#             # cursor.execute(create_students_query)
#
#             # cursor.executemany(insert_rooms_query, room_list)
#             # cursor.executemany(insert_students_query, student_list)
#             cursor.execute(get_amount_in_rooms_query)
#             for string in cursor:
#                 print(string)
#             connection.commit()
#
# except Error as e:
#     print(e)

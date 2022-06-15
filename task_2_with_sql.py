from mysql.connector import *
from getpass import getpass
from services.room_service import *

try:
    with connect(host="localhost", user=input("Username: "), password=getpass("Password: "),
                 database=input("Database: ")) as connection:
        create_db_query = "CREATE DATABASE dorm"
        create_students_query = """CREATE TABLE students(
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                student_id INT,
                                name VARCHAR(30),
                                room_id INT,
                                FOREIGN KEY(room_id) REFERENCES rooms(id)
                                )"""
        create_rooms_query = """CREATE TABLE rooms(
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                room_id INT,
                                name VARCHAR(30)
                                )"""
        insert_students_query = """INSERT INTO students
                                (student_id,name, room_id)
                                VALUES(%s,%s,(SELECT id FROM rooms 
                                                WHERE room_id = %s
                                                LIMIT 1
                                                ))"""
        student_list = RoomService.get_student_list_as_tuples("./resources/input/students.json")
        insert_rooms_query = """INSERT INTO rooms
                                (room_id,name)
                                VALUES(%s,%s)"""
        room_list = RoomService.get_room_list_as_tuples("./resources/input/rooms.json")
        get_amount_in_rooms_query = """SELECT rooms.name, COUNT(student_id) AS amount
                                        FROM students JOIN rooms ON students.room_id = rooms.id
                                        GROUP BY rooms.room_id
                                        ORDER BY rooms.room_id """
        with connection.cursor() as cursor:
            # cursor.execute(create_rooms_query)
            # cursor.execute(create_students_query)

            # cursor.executemany(insert_rooms_query, room_list)
            # cursor.executemany(insert_students_query, student_list)
            cursor.execute(get_amount_in_rooms_query)
            for string in cursor:
                print(string)
            connection.commit()

except Error as e:
    print(e)

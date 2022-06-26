import json
import xml.etree.ElementTree as ElementTree

from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, select, func, Index, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from entities.models import Room, Student


def load_students_from_json_to_db(filepath: str, session: Session):
    with open(filepath) as input_file:
        strings = json.load(input_file)
    for student in strings:
        query = select(Room.id).where(Room.room_id == student["room"])
        session.add(
            Student(birthday=student["birthday"], student_id=student["id"], name=student["name"], room=student["room"],
                    sex=student["sex"],
                    room_id=query.scalar_subquery()))
    session.commit()


def load_rooms_from_json_to_db(filepath: str, session: Session):
    with open(filepath) as input_file:
        strings = json.load(input_file)
    for room in strings:
        session.add(Room(room_id=room["id"], name=room["name"]))
    session.commit()


def _declare_students_table(metadata: MetaData):
    return Table("students", metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('birthday', DateTime()),
                 Column('student_id', Integer),
                 Column('name', String(30)),
                 Column('room', Integer()),
                 Column('sex', String(1)),
                 Column('room_id', ForeignKey("rooms.id"))
                 )


def _declare_rooms_table(metadata: MetaData):
    return Table("rooms", metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('room_id', Integer()),
                 Column('name', String(10))
                 )


def create_indexes(engine: Engine):
    idx_rooms_id = Index("idx_rooms_id", Room.id)
    idx_rooms_id.create(bind=engine)
    idx_students_room_id = Index("idx_students_room_id", Student.room_id)
    idx_students_room_id.create(bind=engine)


def create_empty_tables(metadata: MetaData, engine: Engine):
    _declare_rooms_table(metadata)
    _declare_students_table(metadata)
    metadata.drop_all(engine)
    metadata.create_all(engine)


def save_as_file(output_format: str, dict_list: list, filename: str):
    if str(output_format).upper() == "XML":
        save_as_xml(dict_list, filename)
    if str(output_format).upper() == "JSON":
        save_as_json(dict_list, filename)


def save_as_xml(dict_list: list, filename: str):
    dorm = ElementTree.Element('dorm')
    rooms = ElementTree.SubElement(dorm, "rooms")
    for element in dict_list:
        room = ElementTree.SubElement(rooms, "room")
        for key in element:
            room.set(key, str(element[key]))
    output_file = open(f"./resources/output/{filename}.xml", "w")
    output_file.write(ElementTree.tostring(dorm).decode('utf-8'))


def save_as_json(dict_list: list, filename: str):
    with open(f'./resources/output/{filename}.json', 'w') as output_file:
        json.dump(dict_list, output_file)


def write_amount_in_rooms(output_format: str, session: Session):
    rows = session.query(Room, func.count(Student.id)).join(Student).group_by(Room.id).all()

    dict_list = []
    for room_model, amount in rows:
        dict_list.append({"name": room_model.name, "id": room_model.room_id, "amount": amount})

        save_as_file(output_format, dict_list, "amount_in_rooms")


def write_min_average_age_rooms(output_format: str, session: Session):
    avg_birthday = func.from_days(func.avg(func.to_days(Student.birthday)))
    rows = session.query(Room, avg_birthday).join(Student).group_by(Room.id).order_by(
        avg_birthday.desc()).limit(5)

    dict_list = []
    for room_model, birthday in rows:
        dict_list.append(
            {"name": room_model.name, "id": room_model.room_id, "average_birthday_date": str(birthday)})

    save_as_file(output_format, dict_list, "min_average_age_rooms")


def write_max_age_margin_rooms(output_format: str, session: Session):
    date1 = func.max(Student.birthday)
    date2 = func.min(Student.birthday)
    margin = func.datediff(date1, date2)
    rows = session.query(Room, date1, date2).join(Student).group_by(Room.id).order_by(
        margin.desc()).limit(5)

    dict_list = []
    for room_model, birthday1, birthday2 in rows:
        dict_list.append({"name": room_model.name, "id": room_model.room_id, "max_birthday_date": str(birthday1),
                          "min_birthday_date": str(birthday2)})

    save_as_file(output_format, dict_list, "max_age_margin_rooms")


# почти все, кроме 6, 221, 222, 396, 419,484,579,623,736
def write_mixed_rooms(output_format: str, session: Session):
    table = (select(Room.room_id, Room.name.label("room_name"), Student.sex).join(Student).group_by(Room.id).group_by(
        Student.sex))
    rows = session.query(table.c.room_id, table.c.room_name).group_by(table.c.room_id).having(
        func.count(table.c.sex) == 2)

    dict_list = []
    for room_id, room_name in rows:
        dict_list.append({"id": room_id, "name": room_name})

    save_as_file(output_format, dict_list, "mixed_rooms")

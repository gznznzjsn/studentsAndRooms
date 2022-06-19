from sqlalchemy import create_engine, MetaData, select, func
from sqlalchemy.orm import sessionmaker, query, Session

from entities.models import Room, Student
from services.db_service import load_students_from_json_to_db, load_rooms_from_json_to_db, \
    declare_students_table, declare_rooms_table, write_amount_in_rooms, write_min_average_age_rooms, \
    write_max_age_margin_rooms, write_mixed_rooms

engine = create_engine("mysql+mysqlconnector://root:1q2w3e@localhost/dorm")
metadata = MetaData()
factory = sessionmaker(bind=engine)
session = factory()

# declare_rooms_table(metadata)
# declare_students_table(metadata)
# metadata.drop_all(engine)
# metadata.create_all(engine)
#
#
# load_rooms_from_json_to_db("./resources/input/rooms.json", session)
# load_students_from_json_to_db("./resources/input/students_extended.json", session)

# 1
write_amount_in_rooms("JSON", session)
# 2
write_min_average_age_rooms("JSON", session)
write_max_age_margin_rooms("JSON", session)
write_mixed_rooms("XML", session)

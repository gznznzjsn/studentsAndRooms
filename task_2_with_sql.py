import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from services.db_service import write_amount_in_rooms, write_min_average_age_rooms, \
    write_max_age_margin_rooms, write_mixed_rooms, create_indexes, create_empty_tables, load_students_from_json_to_db, \
    load_rooms_from_json_to_db

load_dotenv()

user = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
database = os.getenv('DATABASE')
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
metadata = MetaData()
factory = sessionmaker(bind=engine)
session = factory()

if input("Do you want to recreate tables and reload all records from json? (Y/N)") == "Y":
    create_empty_tables(metadata, engine)
    create_indexes(engine)
    students = input("Please, enter the path to students_extended.json: ")
    rooms = input("Please, enter the path to rooms.json: ")
    print("wait...")
    load_rooms_from_json_to_db(rooms, session)
    load_students_from_json_to_db(students, session)

output_format = input("Please, enter the output format(JSON/XML): ")
write_amount_in_rooms(output_format, session)
write_min_average_age_rooms(output_format, session)
write_max_age_margin_rooms(output_format, session)
write_mixed_rooms(output_format, session)

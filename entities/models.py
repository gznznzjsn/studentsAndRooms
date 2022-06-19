from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class Student(BaseModel):
    __tablename__ = "students"

    id = Column(Integer(), primary_key=True)
    birthday = Column(DateTime())
    student_id = Column(Integer())
    name = Column(String(30))
    room = Column(Integer())
    sex = Column(String(1))
    room_id = Column(ForeignKey("rooms.id"))


class Room(BaseModel):
    __tablename__ = "rooms"

    id = Column(Integer(), primary_key=True)
    room_id = Column(Integer())
    name = Column(String(10))

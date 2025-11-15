from database import Base
from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean, ForeignKey
from uuid import uuid4
from datetime import datetime



class User(Base):
    __tablename__ = "users"
    id = Column(String, default=lambda: str(uuid4()), primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String) 



class Question(Base):
    __tablename__ = "questions"

    id = Column(String, default=lambda: str(uuid4()), primary_key=True)
    title = Column(String)
    type = Column(String)
    complexity = Column(String)
    options = Column(JSON, nullable=True)
    correct_answers = Column(JSON, nullable=True)
    max_score = Column(Integer, default=1)




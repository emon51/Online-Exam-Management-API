from database import Base
from sqlalchemy import Column, Integer, String, JSON




class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String) 



class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    type = Column(String)
    complexity = Column(String)
    options = Column(JSON, nullable=True)
    correct_answers = Column(JSON, nullable=True)
    max_score = Column(Integer, default=1)

    
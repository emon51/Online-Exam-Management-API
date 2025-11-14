from enum import Enum 
from pydantic import BaseModel, EmailStr
from typing import List, Optional



class Role(str, Enum):
    admin = 'admin'
    student = 'student'

class UserModel(BaseModel):
    username: str 
    email: EmailStr 
    password: str 
    role: Role 


class LoginModel(BaseModel):
    email: EmailStr 
    password: str 


class Complexity(str, Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"

class QuestionModel(BaseModel):
    title: str
    type: str
    complexity: Complexity
    options: Optional[List[str]] = None
    correct_answers: Optional[List[str]] = None
    max_score: int = 1 

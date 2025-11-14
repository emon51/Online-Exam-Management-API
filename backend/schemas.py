from enum import Enum 
from pydantic import BaseModel, EmailStr



class Role(str, Enum):
    admin = 'admin'
    student = 'student'

class UserModel(BaseModel):
    username: str 
    email: EmailStr 
    password: str 
    role: Role 
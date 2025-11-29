from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    password_hash: str
    created_at: datetime
    updated_at: datetime

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime




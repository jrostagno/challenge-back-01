from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    created_at: datetime
    updated_at: datetime
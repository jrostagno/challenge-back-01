from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The name of the user",
        examples=["John Doe"],
    )
    email: EmailStr = Field(
        ..., description="The email of the user", examples=["john.doe@example.com"]
    )


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="The password of the user",
        examples=["password123"],
    )


class UserInDB(UserBase):
    user_id: int
    password_hash: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

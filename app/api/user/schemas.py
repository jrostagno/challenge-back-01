from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


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
        description="The password of the user (max 72 bytes in UTF-8 encoding due to bcrypt limitation. Note: characters with accents or emojis use more bytes)",
        examples=["password123"],
    )

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 72:
            raise ValueError(
                f'Password cannot exceed 72 bytes when encoded in UTF-8. '
                f'Your password has {len(password_bytes)} bytes. '
                f'Note: Characters with accents, emojis, or special symbols may use more than 1 byte each.'
            )
        return v


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

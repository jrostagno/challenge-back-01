from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(
        ..., description="The email of the user", examples=["john.doe@example.com"]
    )
    password: str = Field(
        ...,
        min_length=8,
        description="The password of the user",
        examples=["password123"],
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

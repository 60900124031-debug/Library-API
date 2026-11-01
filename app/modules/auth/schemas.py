from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    member_id: int | None
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
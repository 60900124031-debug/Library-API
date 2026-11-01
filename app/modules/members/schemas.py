from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class MemberResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    joined_at: datetime
    model_config = ConfigDict(from_attributes=True)
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LoanCreate(BaseModel):
    book_id: int
    member_id: int | None = None  # wajib untuk admin, diabaikan untuk member


class LoanResponse(BaseModel):
    id: int
    book_id: int
    member_id: int
    borrowed_at: datetime
    due_date: datetime
    returned_at: datetime | None
    fine: int
    model_config = ConfigDict(from_attributes=True)
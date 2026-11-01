from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    loan_id: int
    amount: int = Field(gt=0)


class PaymentResponse(BaseModel):
    id: int
    loan_id: int
    amount: int
    paid_at: datetime
    model_config = ConfigDict(from_attributes=True)
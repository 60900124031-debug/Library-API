from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    loan_id: Mapped[int] = mapped_column(ForeignKey("loans.id"), unique=True, index=True)
    amount: Mapped[int]
    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.loans.repository import SqlAlchemyLoanRepository
from app.modules.payments.repository import SqlAlchemyPaymentRepository
from app.modules.payments.service import PaymentService


def get_payment_service(db: Session = Depends(get_db)) -> PaymentService:
    return PaymentService(SqlAlchemyPaymentRepository(db), SqlAlchemyLoanRepository(db))
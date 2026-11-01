from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError
from app.modules.loans.models import Loan
from app.modules.payments.models import Payment


class PaymentRepository(ABC):
    @abstractmethod
    def get_by_loan_id(self, loan_id: int) -> Payment | None: ...

    @abstractmethod
    def list_all(self, member_id: int | None) -> list[Payment]: ...

    @abstractmethod
    def count_unpaid_fines_by_member(self, member_id: int) -> int: ...

    @abstractmethod
    def create(self, loan_id: int, amount: int, paid_at: datetime) -> Payment: ...


class SqlAlchemyPaymentRepository(PaymentRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_loan_id(self, loan_id: int) -> Payment | None:
        return self.db.query(Payment).filter(Payment.loan_id == loan_id).first()

    def list_all(self, member_id: int | None) -> list[Payment]:
        query = self.db.query(Payment)
        if member_id is not None:
            query = query.join(Loan, Loan.id == Payment.loan_id).filter(
                Loan.member_id == member_id
            )
        return query.order_by(Payment.id.desc()).all()

    def count_unpaid_fines_by_member(self, member_id: int) -> int:
        return (
            self.db.query(Loan)
            .outerjoin(Payment, Payment.loan_id == Loan.id)
            .filter(Loan.member_id == member_id, Loan.fine > 0, Payment.id.is_(None))
            .count()
        )

    def create(self, loan_id: int, amount: int, paid_at: datetime) -> Payment:
        payment = Payment(loan_id=loan_id, amount=amount, paid_at=paid_at)
        self.db.add(payment)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ConflictError("Denda ini sudah dibayar")
        self.db.refresh(payment)
        return payment
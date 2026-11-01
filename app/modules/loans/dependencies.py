from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.modules.books.repository import SqlAlchemyBookRepository
from app.modules.loans.policies import DailyFinePolicy
from app.modules.loans.repository import SqlAlchemyLoanRepository
from app.modules.loans.service import LoanService
from app.modules.members.repository import SqlAlchemyMemberRepository
from app.modules.payments.repository import SqlAlchemyPaymentRepository


def get_loan_service(db: Session = Depends(get_db)) -> LoanService:
    return LoanService(
        loan_repo=SqlAlchemyLoanRepository(db),
        book_repo=SqlAlchemyBookRepository(db),
        member_repo=SqlAlchemyMemberRepository(db),
        payment_repo=SqlAlchemyPaymentRepository(db),
        fine_policy=DailyFinePolicy(settings.fine_per_day),
        loan_duration_days=settings.loan_duration_days,
        max_active_loans=settings.max_active_loans,
    )
from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy.orm import Session

from app.modules.loans.models import Loan


class LoanRepository(ABC):
    @abstractmethod
    def get_by_id(self, loan_id: int) -> Loan | None: ...

    @abstractmethod
    def count_active_by_member(self, member_id: int) -> int: ...

    @abstractmethod
    def count_overdue_by_member(self, member_id: int, now: datetime) -> int: ...

    @abstractmethod
    def list_by_member(self, member_id: int) -> list[Loan]: ...

    @abstractmethod
    def list_overdue(self, now: datetime) -> list[Loan]: ...

    @abstractmethod
    def create(
        self, book_id: int, member_id: int, borrowed_at: datetime, due_date: datetime
    ) -> Loan: ...

    @abstractmethod
    def mark_returned(self, loan: Loan, returned_at: datetime, fine: int) -> Loan: ...


class SqlAlchemyLoanRepository(LoanRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, loan_id: int) -> Loan | None:
        return self.db.get(Loan, loan_id)

    def count_active_by_member(self, member_id: int) -> int:
        return (
            self.db.query(Loan)
            .filter(Loan.member_id == member_id, Loan.returned_at.is_(None))
            .count()
        )

    def count_overdue_by_member(self, member_id: int, now: datetime) -> int:
        return (
            self.db.query(Loan)
            .filter(
                Loan.member_id == member_id,
                Loan.returned_at.is_(None),
                Loan.due_date < now,
            )
            .count()
        )

    def list_by_member(self, member_id: int) -> list[Loan]:
        return (
            self.db.query(Loan)
            .filter(Loan.member_id == member_id)
            .order_by(Loan.id.desc())
            .all()
        )

    def list_overdue(self, now: datetime) -> list[Loan]:
        return (
            self.db.query(Loan)
            .filter(Loan.returned_at.is_(None), Loan.due_date < now)
            .order_by(Loan.due_date)
            .all()
        )

    def create(
        self, book_id: int, member_id: int, borrowed_at: datetime, due_date: datetime
    ) -> Loan:
        loan = Loan(
            book_id=book_id,
            member_id=member_id,
            borrowed_at=borrowed_at,
            due_date=due_date,
        )
        self.db.add(loan)
        self.db.commit()  # sekaligus menyimpan perubahan stok buku (Session yang sama)
        self.db.refresh(loan)
        return loan

    def mark_returned(self, loan: Loan, returned_at: datetime, fine: int) -> Loan:
        loan.returned_at = returned_at
        loan.fine = fine
        self.db.commit()  # sekaligus menyimpan penambahan stok (Session yang sama)
        self.db.refresh(loan)
        return loan
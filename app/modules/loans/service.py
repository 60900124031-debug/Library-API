from datetime import datetime, timedelta, timezone

from app.core.exceptions import (
    BusinessRuleError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
)
from app.modules.books.repository import BookRepository
from app.modules.loans.models import Loan
from app.modules.loans.policies import FinePolicy
from app.modules.loans.repository import LoanRepository
from app.modules.loans.schemas import LoanCreate
from app.modules.members.repository import MemberRepository
from app.modules.payments.repository import PaymentRepository


class LoanService:
    def __init__(
        self,
        loan_repo: LoanRepository,
        book_repo: BookRepository,
        member_repo: MemberRepository,
        payment_repo: PaymentRepository,
        fine_policy: FinePolicy,
        loan_duration_days: int,
        max_active_loans: int,
    ):
        self.loan_repo = loan_repo
        self.book_repo = book_repo
        self.member_repo = member_repo
        self.payment_repo = payment_repo
        self.fine_policy = fine_policy
        self.loan_duration_days = loan_duration_days
        self.max_active_loans = max_active_loans

    def borrow_book(self, data: LoanCreate, member_scope: int | None) -> Loan:
        now = datetime.now(timezone.utc)

        if member_scope is not None:
            if data.member_id not in (None, member_scope):
                raise ForbiddenError("Anda hanya boleh meminjam atas nama sendiri")
            member_id = member_scope
        elif data.member_id is None:
            raise BusinessRuleError("Admin wajib mengisi member_id")
        else:
            member_id = data.member_id

        member = self.member_repo.get_by_id(member_id)
        if member is None:
            raise NotFoundError(f"Anggota dengan id {member_id} tidak ditemukan")

        book = self.book_repo.get_by_id_for_update(data.book_id)
        if book is None:
            raise NotFoundError(f"Buku dengan id {data.book_id} tidak ditemukan")

        if book.stock < 1:
            raise BusinessRuleError(f"Stok buku '{book.title}' sedang habis")

        if self.loan_repo.count_overdue_by_member(member.id, now) > 0:
            raise BusinessRuleError(
                "Anggota masih memiliki pinjaman terlambat, kembalikan dulu"
            )

        if self.payment_repo.count_unpaid_fines_by_member(member.id) > 0:
            raise BusinessRuleError("Anggota masih memiliki denda yang belum dibayar")

        if self.loan_repo.count_active_by_member(member.id) >= self.max_active_loans:
            raise BusinessRuleError(
                f"Batas maksimal {self.max_active_loans} pinjaman aktif tercapai"
            )

        self.book_repo.decrease_stock(book)
        due_date = now + timedelta(days=self.loan_duration_days)
        return self.loan_repo.create(book.id, member.id, now, due_date)

    def return_book(self, loan_id: int) -> Loan:
        loan = self.loan_repo.get_by_id(loan_id)
        if loan is None:
            raise NotFoundError(f"Peminjaman dengan id {loan_id} tidak ditemukan")
        if loan.returned_at is not None:
            raise ConflictError("Buku ini sudah dikembalikan")

        now = datetime.now(timezone.utc)
        fine = self.fine_policy.calculate(loan.due_date, now)

        book = self.book_repo.get_by_id_for_update(loan.book_id)
        self.book_repo.increase_stock(book)
        return self.loan_repo.mark_returned(loan, now, fine)

    def list_member_loans(self, member_id: int, member_scope: int | None) -> list[Loan]:
        if member_scope is not None and member_scope != member_id:
            raise ForbiddenError("Anda hanya boleh melihat pinjaman milik sendiri")
        if self.member_repo.get_by_id(member_id) is None:
            raise NotFoundError(f"Anggota dengan id {member_id} tidak ditemukan")
        return self.loan_repo.list_by_member(member_id)

    def list_overdue(self) -> list[Loan]:
        return self.loan_repo.list_overdue(datetime.now(timezone.utc))
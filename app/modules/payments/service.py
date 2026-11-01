from datetime import datetime, timezone

from app.core.exceptions import (
    BusinessRuleError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
)
from app.modules.loans.repository import LoanRepository
from app.modules.payments.models import Payment
from app.modules.payments.repository import PaymentRepository
from app.modules.payments.schemas import PaymentCreate


class PaymentService:
    def __init__(self, payment_repo: PaymentRepository, loan_repo: LoanRepository):
        self.payment_repo = payment_repo
        self.loan_repo = loan_repo

    def pay_fine(self, data: PaymentCreate, member_scope: int | None) -> Payment:
        loan = self.loan_repo.get_by_id(data.loan_id)
        if loan is None:
            raise NotFoundError(f"Peminjaman dengan id {data.loan_id} tidak ditemukan")
        if member_scope is not None and loan.member_id != member_scope:
            raise ForbiddenError("Anda hanya boleh membayar denda milik sendiri")
        if loan.returned_at is None:
            raise BusinessRuleError("Buku belum dikembalikan, denda belum final")
        if loan.fine <= 0:
            raise BusinessRuleError("Peminjaman ini tidak memiliki denda")
        if self.payment_repo.get_by_loan_id(loan.id):
            raise ConflictError("Denda ini sudah dibayar")
        if data.amount != loan.fine:
            raise BusinessRuleError(
                f"Jumlah pembayaran harus sama dengan denda: Rp{loan.fine}"
            )
        return self.payment_repo.create(loan.id, data.amount, datetime.now(timezone.utc))

    def list_payments(self, member_scope: int | None) -> list[Payment]:
        return self.payment_repo.list_all(member_scope)

from fastapi import APIRouter, Depends

from app.modules.auth.dependencies import (
    get_member_scope,
    require_admin,
)
from app.modules.auth.models import User
from app.modules.loans.dependencies import get_loan_service
from app.modules.loans.schemas import LoanCreate, LoanResponse
from app.modules.loans.service import LoanService

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/", response_model=LoanResponse, status_code=201)
def borrow_book(
    data: LoanCreate,
    service: LoanService = Depends(get_loan_service),
    member_scope: int | None = Depends(get_member_scope),
):
    return service.borrow_book(data, member_scope)


@router.post("/{loan_id}/return", response_model=LoanResponse)
def return_book(
    loan_id: int,
    service: LoanService = Depends(get_loan_service),
    admin: User = Depends(require_admin),
):
    return service.return_book(loan_id)


@router.get("/member/{member_id}", response_model=list[LoanResponse])
def list_member_loans(
    member_id: int,
    service: LoanService = Depends(get_loan_service),
    member_scope: int | None = Depends(get_member_scope),
):
    return service.list_member_loans(member_id, member_scope)


@router.get("/overdue", response_model=list[LoanResponse])
def list_overdue(
    service: LoanService = Depends(get_loan_service),
    admin: User = Depends(require_admin),
):
    return service.list_overdue()

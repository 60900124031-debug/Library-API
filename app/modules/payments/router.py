from fastapi import APIRouter, Depends, status

from app.modules.auth.dependencies import get_member_scope
from app.modules.payments.dependencies import get_payment_service
from app.modules.payments.schemas import PaymentCreate, PaymentResponse
from app.modules.payments.service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def pay_fine(
    data: PaymentCreate,
    scope: int | None = Depends(get_member_scope),
    service: PaymentService = Depends(get_payment_service),
):
    return service.pay_fine(data, scope)


@router.get("", response_model=list[PaymentResponse])
def list_payments(
    scope: int | None = Depends(get_member_scope),
    service: PaymentService = Depends(get_payment_service),
):
    return service.list_payments(scope)
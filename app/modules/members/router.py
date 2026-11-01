from fastapi import APIRouter, Depends, Query, status

from app.modules.members.dependencies import get_member_service
from app.modules.members.schemas import MemberCreate, MemberResponse
from app.modules.members.service import MemberService

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(
    data: MemberCreate, service: MemberService = Depends(get_member_service)
):
    return service.register(data)


@router.get("", response_model=list[MemberResponse])
def list_members(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    service: MemberService = Depends(get_member_service),
):
    return service.list_members(skip, limit)


@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, service: MemberService = Depends(get_member_service)):
    return service.get_member(member_id)
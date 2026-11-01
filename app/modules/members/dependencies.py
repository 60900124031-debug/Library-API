from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.members.repository import SqlAlchemyMemberRepository
from app.modules.members.service import MemberService


def get_member_service(db: Session = Depends(get_db)) -> MemberService:
    return MemberService(SqlAlchemyMemberRepository(db))
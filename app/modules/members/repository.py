from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.modules.members.models import Member
from app.modules.members.schemas import MemberCreate


class MemberRepository(ABC):
    @abstractmethod
    def get_all(self, skip: int, limit: int) -> list[Member]: ...

    @abstractmethod
    def get_by_id(self, member_id: int) -> Member | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> Member | None: ...

    @abstractmethod
    def create(self, data: MemberCreate) -> Member: ...


class SqlAlchemyMemberRepository(MemberRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int, limit: int) -> list[Member]:
        return self.db.query(Member).order_by(Member.id).offset(skip).limit(limit).all()

    def get_by_id(self, member_id: int) -> Member | None:
        return self.db.get(Member, member_id)

    def get_by_email(self, email: str) -> Member | None:
        return self.db.query(Member).filter(Member.email == email).first()

    def create(self, data: MemberCreate) -> Member:
        member = Member(**data.model_dump())
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member
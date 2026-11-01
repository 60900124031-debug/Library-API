from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.modules.auth.models import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    def create(
        self, username: str, hashed_password: str, role: str, member_id: int | None
    ) -> User: ...


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create(
        self, username: str, hashed_password: str, role: str, member_id: int | None
    ) -> User:
        user = User(
            username=username,
            hashed_password=hashed_password,
            role=role,
            member_id=member_id,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
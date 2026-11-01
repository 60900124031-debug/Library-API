from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import ForbiddenError
from app.modules.auth.models import Role, User
from app.modules.auth.repository import SqlAlchemyUserRepository
from app.modules.auth.service import AuthService
from app.modules.members.repository import SqlAlchemyMemberRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(SqlAlchemyUserRepository(db), SqlAlchemyMemberRepository(db))


def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(get_auth_service),
) -> User:
    return service.get_user_from_token(token)


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != Role.ADMIN:
        raise ForbiddenError("Hanya admin yang boleh mengakses endpoint ini")
    return user


def get_member_scope(user: User = Depends(get_current_user)) -> int | None:
    """None = admin (tanpa batasan). Angka = hanya data milik member_id tersebut."""
    if user.role == Role.ADMIN:
        return None
    if user.member_id is None:
        raise ForbiddenError("Akun ini tidak terhubung ke data anggota")
    return user.member_id
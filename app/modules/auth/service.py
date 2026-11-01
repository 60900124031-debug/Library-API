from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.modules.auth.models import Role, User
from app.modules.auth.repository import UserRepository
from app.modules.auth.schemas import RegisterRequest
from app.modules.members.repository import MemberRepository
from app.modules.members.schemas import MemberCreate


class AuthService:
    def __init__(self, repository: UserRepository, member_repo: MemberRepository):
        self.repository = repository
        self.member_repo = member_repo

    def register(self, data: RegisterRequest) -> User:
        if self.repository.get_by_username(data.username):
            raise ConflictError(f"Username {data.username} sudah dipakai")
        if self.member_repo.get_by_email(data.email):
            raise ConflictError(f"Email {data.email} sudah terdaftar")

        member = self.member_repo.create(MemberCreate(name=data.name, email=data.email))
        # Role SELALU member, tidak pernah dari request
        return self.repository.create(
            data.username, hash_password(data.password), Role.MEMBER, member.id
        )

    def login(self, username: str, password: str) -> str:
        user = self.repository.get_by_username(username)
        if user is None or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Username atau password salah")
        return create_access_token(user.username)

    def get_user_from_token(self, token: str) -> User:
        username = decode_access_token(token)
        user = self.repository.get_by_username(username)
        if user is None:
            raise UnauthorizedError("Token tidak valid atau sudah kedaluwarsa")
        return user
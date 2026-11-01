from app.core.exceptions import ConflictError, NotFoundError
from app.modules.members.models import Member
from app.modules.members.repository import MemberRepository
from app.modules.members.schemas import MemberCreate


class MemberService:
    def __init__(self, repository: MemberRepository):
        self.repository = repository

    def register(self, data: MemberCreate) -> Member:
        if self.repository.get_by_email(data.email):
            raise ConflictError(f"Email {data.email} sudah terdaftar")
        return self.repository.create(data)

    def get_member(self, member_id: int) -> Member:
        member = self.repository.get_by_id(member_id)
        if member is None:
            raise NotFoundError(f"Anggota dengan id {member_id} tidak ditemukan")
        return member

    def list_members(self, skip: int, limit: int) -> list[Member]:
        return self.repository.get_all(skip, limit)
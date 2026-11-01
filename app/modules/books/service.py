from app.core.exceptions import ConflictError, NotFoundError
from app.modules.books.models import Book
from app.modules.books.repository import BookRepository
from app.modules.books.schemas import BookCreate, BookUpdate


class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def list_books(self, keyword: str | None, skip: int, limit: int) -> list[Book]:
        return self.repository.search(keyword, skip, limit)

    def get_book(self, book_id: int) -> Book:
        book = self.repository.get_by_id(book_id)
        if book is None:
            raise NotFoundError(f"Buku dengan id {book_id} tidak ditemukan")
        return book

    def create_book(self, data: BookCreate) -> Book:
        if self.repository.get_by_isbn(data.isbn):
            raise ConflictError(f"ISBN {data.isbn} sudah terdaftar")
        return self.repository.create(data)

    def update_book(self, book_id: int, data: BookUpdate) -> Book:
        book = self.get_book(book_id)
        return self.repository.update(book, data)

    def delete_book(self, book_id: int) -> None:
        book = self.get_book(book_id)
        self.repository.delete(book)
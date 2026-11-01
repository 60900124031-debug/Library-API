from abc import ABC, abstractmethod

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.modules.books.models import Book
from app.modules.books.schemas import BookCreate, BookUpdate


class BookRepository(ABC):
    @abstractmethod
    def search(self, keyword: str | None, skip: int, limit: int) -> list[Book]: ...

    @abstractmethod
    def get_by_id(self, book_id: int) -> Book | None: ...

    @abstractmethod
    def get_by_id_for_update(self, book_id: int) -> Book | None: ...

    @abstractmethod
    def get_by_isbn(self, isbn: str) -> Book | None: ...

    @abstractmethod
    def create(self, data: BookCreate) -> Book: ...

    @abstractmethod
    def update(self, book: Book, data: BookUpdate) -> Book: ...

    @abstractmethod
    def delete(self, book: Book) -> None: ...

    @abstractmethod
    def decrease_stock(self, book: Book) -> None: ...

    @abstractmethod
    def increase_stock(self, book: Book) -> None: ...


class SqlAlchemyBookRepository(BookRepository):
    def __init__(self, db: Session):
        self.db = db

    def search(self, keyword: str | None, skip: int, limit: int) -> list[Book]:
        query = self.db.query(Book)
        if keyword:
            like = f"%{keyword}%"
            query = query.filter(or_(Book.title.ilike(like), Book.author.ilike(like)))
        return query.order_by(Book.id).offset(skip).limit(limit).all()

    def get_by_id(self, book_id: int) -> Book | None:
        return self.db.get(Book, book_id)

    def get_by_id_for_update(self, book_id: int) -> Book | None:
        # Kunci baris agar dua peminjaman bersamaan tidak berebut stok terakhir
        return self.db.get(Book, book_id, with_for_update=True)

    def get_by_isbn(self, isbn: str) -> Book | None:
        return self.db.query(Book).filter(Book.isbn == isbn).first()

    def create(self, data: BookCreate) -> Book:
        book = Book(**data.model_dump())
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def update(self, book: Book, data: BookUpdate) -> Book:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(book, key, value)
        self.db.commit()
        self.db.refresh(book)
        return book

    def delete(self, book: Book) -> None:
        self.db.delete(book)
        self.db.commit()

    def decrease_stock(self, book: Book) -> None:
        book.stock -= 1  # commit dilakukan LoanRepository (satu transaksi)

    def increase_stock(self, book: Book) -> None:
        book.stock += 1
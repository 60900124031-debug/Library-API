from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.books.repository import SqlAlchemyBookRepository
from app.modules.books.service import BookService


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(SqlAlchemyBookRepository(db))
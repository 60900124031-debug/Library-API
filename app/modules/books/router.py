from fastapi import APIRouter, Depends, Query, status

from app.modules.auth.dependencies import require_admin
from app.modules.books.dependencies import get_book_service
from app.modules.books.schemas import BookCreate, BookResponse, BookUpdate
from app.modules.books.service import BookService

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=list[BookResponse])
def list_books(
    q: str | None = Query(default=None, description="Cari judul/penulis"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    service: BookService = Depends(get_book_service),
):
    return service.list_books(q, skip, limit)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, service: BookService = Depends(get_book_service)):
    return service.get_book(book_id)


@router.post(
    "",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_book(data: BookCreate, service: BookService = Depends(get_book_service)):
    return service.create_book(data)


@router.patch(
    "/{book_id}", response_model=BookResponse, dependencies=[Depends(require_admin)]
)
def update_book(
    book_id: int, data: BookUpdate, service: BookService = Depends(get_book_service)
):
    return service.update_book(book_id, data)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_book(book_id: int, service: BookService = Depends(get_book_service)):
    service.delete_book(book_id)
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.core.database import Base, engine
from app.core.exceptions import DomainError
from app.modules.auth import models as auth_models  # noqa: F401
from app.modules.auth.dependencies import get_current_user, require_admin
from app.modules.auth.router import router as auth_router
from app.modules.books import models as book_models  # noqa: F401
from app.modules.books.router import router as books_router
from app.modules.loans import models as loan_models  # noqa: F401
from app.modules.loans.router import router as loans_router
from app.modules.members import models as member_models  # noqa: F401
from app.modules.members.router import router as members_router
from app.modules.payments import models as payment_models  # noqa: F401
from app.modules.payments.router import router as payments_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API", version="1.0.0")


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    headers = {"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else None
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.message}, headers=headers
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    # Pengaman terakhir: constraint unik atau relasi dilanggar (misalnya hapus buku yang pernah dipinjam)
    return JSONResponse(
        status_code=409,
        content={"detail": "Data duplikat atau masih dipakai oleh data lain"},
    )


protected = [Depends(get_current_user)]

app.include_router(auth_router)
app.include_router(books_router, dependencies=protected)
app.include_router(members_router, dependencies=[Depends(require_admin)])
app.include_router(loans_router, dependencies=protected)
app.include_router(payments_router, dependencies=protected)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Library API berjalan"}
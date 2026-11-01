from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.modules.auth.dependencies import get_auth_service, get_current_user
from app.modules.auth.models import User
from app.modules.auth.schemas import RegisterRequest, Token, UserResponse
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(data: RegisterRequest, service: AuthService = Depends(get_auth_service)):
    return service.register(data)


@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    return Token(access_token=service.login(form.username, form.password))


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
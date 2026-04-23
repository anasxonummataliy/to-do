from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.auth import Token, LoginRequest, RefreshTokenRequest
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["🔐 Auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yangi foydalanuvchi ro'yxatdan o'tkazish",
)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """
    Yangi foydalanuvchi ro'yxatdan o'tkazadi.
    - **email**: Unikal email manzil
    - **username**: Unikal foydalanuvchi nomi (3-50 belgi)
    - **password**: Kamida 8 belgi, 1 raqam va 1 katta harf
    """
    service = AuthService(db)
    user = service.register(data)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Tizimga kirish",
)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Email va parol bilan tizimga kiradi.
    Access token va refresh token qaytaradi.
    """
    service = AuthService(db)
    return service.login(data)


@router.post(
    "/refresh",
    response_model=Token,
    summary="Token yangilash",
)
def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Refresh token orqali yangi access token oladi.
    """
    service = AuthService(db)
    return service.refresh_tokens(data)

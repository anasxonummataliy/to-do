from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.exceptions import (
    AlreadyExistsException,
    UnauthorizedException,
    BadRequestException,
)
from app.database.models import User
from app.repositories import UserRepository
from app.schemas.auth import Token, LoginRequest, RefreshTokenRequest
from app.schemas.user import UserCreate


class AuthService:
    """Autentifikatsiya va avtorizatsiya service."""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, data: UserCreate) -> User:
        """
        Yangi foydalanuvchi ro'yxatdan o'tkazadi.
        Email yoki username band bo'lsa xato qaytaradi.
        """
        if self.user_repo.email_exists(data.email):
            raise AlreadyExistsException(f"Email '{data.email}' already registered")

        if self.user_repo.username_exists(data.username):
            raise AlreadyExistsException(f"Username '{data.username}' already taken")

        user = User(
            email=data.email,
            username=data.username,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
        )
        return self.user_repo.create(user)

    def login(self, data: LoginRequest) -> Token:
        """
        Email va parol bilan tizimga kiradi.
        Access va refresh token qaytaradi.
        """
        user = self.user_repo.get_by_email(data.email)

        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")

        if not user.is_active:
            raise UnauthorizedException("Account is deactivated")

        return Token(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    def refresh_tokens(self, data: RefreshTokenRequest) -> Token:
        """
        Refresh token orqali yangi token juftligini qaytaradi.
        """
        payload = decode_token(data.refresh_token)

        if not payload or payload.get("type") != "refresh":
            raise BadRequestException("Invalid or expired refresh token")

        user_id = payload.get("sub")
        user = self.user_repo.get_by_id(int(user_id))

        if not user or not user.is_active:
            raise UnauthorizedException("User not found or inactive")

        return Token(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

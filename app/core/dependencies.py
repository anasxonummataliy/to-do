from typing import Generator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.db.session import SessionLocal
from app.models.user import User
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db() -> Generator[Session, None, None]:
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Joriy autentifikatsiya qilingan foydalanuvchini qaytaradi."""
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise UnauthorizedException("Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token payload")

    repo = UserRepository(db)
    user = repo.get_by_id(int(user_id))
    if not user:
        raise UnauthorizedException("User not found")

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Faol foydalanuvchini qaytaradi."""
    if not current_user.is_active:
        raise ForbiddenException("Inactive user")
    return current_user

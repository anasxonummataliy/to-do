from typing import Optional
from sqlalchemy.orm import Session

from app.database.models import User
from app.repositories import BaseRepository


class UserRepository(BaseRepository[User]):
    """Foydalanuvchi uchun repository."""

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        """Email bo'yicha foydalanuvchi topadi."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Username bo'yicha foydalanuvchi topadi."""
        return self.db.query(User).filter(User.username == username).first()

    def email_exists(self, email: str) -> bool:
        """Email mavjudligini tekshiradi."""
        return self.db.query(User.id).filter(User.email == email).scalar() is not None

    def username_exists(self, username: str) -> bool:
        """Username mavjudligini tekshiradi."""
        return (
            self.db.query(User.id).filter(User.username == username).scalar()
            is not None
        )

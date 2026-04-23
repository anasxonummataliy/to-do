from sqlalchemy.orm import Session

from app.core.security import verify_password, hash_password
from app.core.exceptions import (
    NotFoundException,
    AlreadyExistsException,
    BadRequestException,
)
from app.database.models import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserUpdate, UserPasswordUpdate


class UserService:
    """Foydalanuvchi bilan ishlash service."""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def get_profile(self, user_id: int) -> User:
        """Foydalanuvchi profilini qaytaradi."""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return user

    def update_profile(self, user: User, data: UserUpdate) -> User:
        """Foydalanuvchi ma'lumotlarini yangilaydi."""
        if data.email and data.email != user.email:
            if self.user_repo.email_exists(data.email):
                raise AlreadyExistsException("Email already in use")
            user.email = data.email

        if data.full_name is not None:
            user.full_name = data.full_name

        return self.user_repo.update(user)

    def change_password(self, user: User, data: UserPasswordUpdate) -> User:
        """Foydalanuvchi parolini o'zgartiradi."""
        if not verify_password(data.current_password, user.hashed_password):
            raise BadRequestException("Current password is incorrect")

        user.hashed_password = hash_password(data.new_password)
        return self.user_repo.update(user)

    def deactivate_account(self, user: User) -> User:
        """Foydalanuvchi hisobini o'chiradi (soft delete)."""
        user.is_active = False
        return self.user_repo.update(user)

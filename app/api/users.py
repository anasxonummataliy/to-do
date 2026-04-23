from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_active_user
from app.database.models import User
from app.schemas.user import UserResponse, UserUpdate, UserPasswordUpdate
from app.services import UserService

router = APIRouter(prefix="/users", tags=["👤 Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Mening profilim",
)
def get_my_profile(current_user: User = Depends(get_current_active_user)):
    """Joriy foydalanuvchi ma'lumotlarini qaytaradi."""
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Profilni yangilash",
)
def update_my_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Foydalanuvchi profil ma'lumotlarini yangilaydi."""
    service = UserService(db)
    return service.update_profile(current_user, data)


@router.put(
    "/me/password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Parolni o'zgartirish",
)
def change_password(
    data: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Foydalanuvchi parolini o'zgartiradi."""
    service = UserService(db)
    service.change_password(current_user, data)


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Hisobni o'chirish",
)
def deactivate_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Foydalanuvchi hisobini deaktivatsiya qiladi (soft delete)."""
    service = UserService(db)
    service.deactivate_account(current_user)

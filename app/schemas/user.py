from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


# ─── Base ──────────────────────────────────────────────────────────────────────


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)


# ─── Create ────────────────────────────────────────────────────────────────────


class UserCreate(UserBase):
    """Foydalanuvchi ro'yxatdan o'tish schema."""

    password: str = Field(..., min_length=8, max_length=50)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v


# ─── Update ────────────────────────────────────────────────────────────────────


class UserUpdate(BaseModel):
    """Foydalanuvchi ma'lumotlarini yangilash schema."""

    full_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None


class UserPasswordUpdate(BaseModel):
    """Parolni yangilash schema."""

    current_password: str
    new_password: str = Field(..., min_length=8, max_length=50)


# ─── Response ──────────────────────────────────────────────────────────────────


class UserResponse(UserBase):
    """Foydalanuvchi javob schema."""

    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserPublic(BaseModel):
    """Ommaviy foydalanuvchi ma'lumotlari."""

    id: int
    username: str
    full_name: Optional[str] = None

    model_config = {"from_attributes": True}

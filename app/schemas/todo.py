from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.database.models import Priority


# ─── Base ──────────────────────────────────────────────────────────────────────


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Priority = Priority.MEDIUM


# ─── Create ────────────────────────────────────────────────────────────────────


class TodoCreate(TodoBase):
    """Yangi todo yaratish schema."""

    pass


# ─── Update ────────────────────────────────────────────────────────────────────


class TodoUpdate(BaseModel):
    """Todo yangilash schema (barcha maydonlar optional)."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Optional[Priority] = None
    is_completed: Optional[bool] = None


# ─── Response ──────────────────────────────────────────────────────────────────


class TodoResponse(TodoBase):
    """Todo javob schema."""

    id: int
    is_completed: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ─── List Response ─────────────────────────────────────────────────────────────


class TodoListResponse(BaseModel):
    """Sahifalangan todo ro'yxati."""

    items: list[TodoResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

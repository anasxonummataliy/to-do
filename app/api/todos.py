from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_active_user
from app.database.models import Priority
from app.database.models import User
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse
from app.services.todo_services import TodoService

router = APIRouter(prefix="/todos", tags=["✅ Todos"])


@router.post(
    "/",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yangi todo yaratish",
)
def create_todo(
    data: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Yangi todo yaratadi."""
    service = TodoService(db)
    return service.create_todo(data, current_user)


@router.get(
    "/",
    response_model=TodoListResponse,
    summary="Barcha todo'larni olish",
)
def get_todos(
    page: int = Query(1, ge=1, description="Sahifa raqami"),
    page_size: int = Query(20, ge=1, le=100, description="Sahifadagi elementlar soni"),
    is_completed: Optional[bool] = Query(None, description="Bajarilganlik holati"),
    priority: Optional[Priority] = Query(None, description="Muhimlik darajasi"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Foydalanuvchining todo'larini filterlash va sahifalash bilan qaytaradi."""
    service = TodoService(db)
    return service.get_todos(current_user, page, page_size, is_completed, priority)


@router.get(
    "/stats",
    summary="Todo statistikasi",
)
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Foydalanuvchi todo statistikasini qaytaradi."""
    service = TodoService(db)
    return service.get_stats(current_user)


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Bitta todo olish",
)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """ID bo'yicha bitta todo'ni qaytaradi."""
    service = TodoService(db)
    return service.get_todo(todo_id, current_user)


@router.patch(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Todo yangilash",
)
def update_todo(
    todo_id: int,
    data: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Todo ma'lumotlarini yangilaydi (faqat yuborilgan maydonlar)."""
    service = TodoService(db)
    return service.update_todo(todo_id, data, current_user)


@router.patch(
    "/{todo_id}/toggle",
    response_model=TodoResponse,
    summary="Bajarilganlik holatini almashtirish",
)
def toggle_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Todo'ni bajarilgan/bajarilmagan holatiga o'tkazadi."""
    service = TodoService(db)
    return service.toggle_complete(todo_id, current_user)


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Todo o'chirish",
)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Todo'ni o'chiradi."""
    service = TodoService(db)
    service.delete_todo(todo_id, current_user)

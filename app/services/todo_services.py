import math
from typing import Optional
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, ForbiddenException
from app.database.models import Todo, Priority
from app.database.models import User
from app.repositories import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate, TodoListResponse, TodoResponse


class TodoService:
    """Todo bilan ishlash service."""

    def __init__(self, db: Session):
        self.db = db
        self.todo_repo = TodoRepository(db)

    def create_todo(self, data: TodoCreate, owner: User) -> Todo:
        """Yangi todo yaratadi."""
        todo = Todo(
            title=data.title,
            description=data.description,
            priority=data.priority,
            owner_id=owner.id,
        )
        return self.todo_repo.create(todo)

    def get_todos(
        self,
        owner: User,
        page: int = 1,
        page_size: int = 20,
        is_completed: Optional[bool] = None,
        priority: Optional[Priority] = None,
    ) -> TodoListResponse:
        """Foydalanuvchi todo'larini sahifalab qaytaradi."""
        skip = (page - 1) * page_size
        items, total = self.todo_repo.get_by_owner(
            owner_id=owner.id,
            skip=skip,
            limit=page_size,
            is_completed=is_completed,
            priority=priority,
        )
        total_pages = math.ceil(total / page_size) if total > 0 else 1

        return TodoListResponse(
            items=[TodoResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    def get_todo(self, todo_id: int, owner: User) -> Todo:
        """Bitta todo'ni qaytaradi (ownership tekshiradi)."""
        todo = self.todo_repo.get_by_id_and_owner(todo_id, owner.id)
        if not todo:
            raise NotFoundException(f"Todo #{todo_id} not found")
        return todo

    def update_todo(self, todo_id: int, data: TodoUpdate, owner: User) -> Todo:
        """Todo'ni yangilaydi."""
        todo = self.get_todo(todo_id, owner)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)

        return self.todo_repo.update(todo)

    def delete_todo(self, todo_id: int, owner: User) -> None:
        """Todo'ni o'chiradi."""
        todo = self.get_todo(todo_id, owner)
        self.todo_repo.delete(todo)

    def toggle_complete(self, todo_id: int, owner: User) -> Todo:
        """Todo'ni bajarilgan/bajarilmagan holatini o'zgartiradi."""
        todo = self.get_todo(todo_id, owner)
        todo.is_completed = not todo.is_completed
        return self.todo_repo.update(todo)

    def get_stats(self, owner: User) -> dict:
        """Foydalanuvchi todo statistikasini qaytaradi."""
        total = self.todo_repo.count_by_owner(owner.id)
        completed = self.todo_repo.count_completed_by_owner(owner.id)
        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "completion_rate": round(completed / total * 100, 1) if total > 0 else 0,
        }

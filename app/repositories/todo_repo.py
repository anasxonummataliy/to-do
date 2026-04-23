from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database.models.todo import Todo, Priority
from app.repositories.base_repo import BaseRepository


class TodoRepository(BaseRepository[Todo]):
    """Todo uchun repository."""

    def __init__(self, db: Session):
        super().__init__(Todo, db)

    def get_by_owner(
        self,
        owner_id: int,
        skip: int = 0,
        limit: int = 20,
        is_completed: Optional[bool] = None,
        priority: Optional[Priority] = None,
    ) -> Tuple[List[Todo], int]:
        """
        Foydalanuvchi todo'larini filterlash bilan qaytaradi.
        (items, total_count) tuple qaytaradi.
        """
        query = self.db.query(Todo).filter(Todo.owner_id == owner_id)

        if is_completed is not None:
            query = query.filter(Todo.is_completed == is_completed)

        if priority is not None:
            query = query.filter(Todo.priority == priority)

        total = query.count()
        items = query.order_by(Todo.created_at.desc()).offset(skip).limit(limit).all()

        return items, total

    def get_by_id_and_owner(self, todo_id: int, owner_id: int) -> Optional[Todo]:
        """ID va owner_id bo'yicha todo topadi (xavfsiz)."""
        return (
            self.db.query(Todo)
            .filter(and_(Todo.id == todo_id, Todo.owner_id == owner_id))
            .first()
        )

    def count_by_owner(self, owner_id: int) -> int:
        """Foydalanuvchining jami todo soni."""
        return self.db.query(Todo).filter(Todo.owner_id == owner_id).count()

    def count_completed_by_owner(self, owner_id: int) -> int:
        """Foydalanuvchining bajarilgan todo soni."""
        return (
            self.db.query(Todo)
            .filter(and_(Todo.owner_id == owner_id, Todo.is_completed == True))
            .count()
        )

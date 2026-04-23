from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic CRUD repository.
    Barcha repository shu classdan meros oladi.
    """

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """ID bo'yicha bitta obyekt qaytaradi."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Sahifalangan barcha obyektlarni qaytaradi."""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def count(self) -> int:
        """Jami obyektlar sonini qaytaradi."""
        return self.db.query(self.model).count()

    def create(self, obj: ModelType) -> ModelType:
        """Yangi obyekt yaratadi."""
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelType) -> ModelType:
        """Obyektni yangilaydi."""
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        """Obyektni o'chiradi."""
        self.db.delete(obj)
        self.db.commit()

    def bulk_create(self, objects: List[ModelType]) -> List[ModelType]:
        """Ko'p obyektni bir vaqtda yaratadi."""
        self.db.add_all(objects)
        self.db.commit()
        for obj in objects:
            self.db.refresh(obj)
        return objects

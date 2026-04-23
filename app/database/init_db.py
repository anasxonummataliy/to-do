from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import engine

# Import all models so Alembic can detect them
from app.models.user import User  # noqa: F401
from app.models.todo import Todo  # noqa: F401


def create_tables() -> None:
    """Barcha jadvallarni yaratadi (development uchun)."""
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    """Barcha jadvallarni o'chiradi (testing uchun)."""
    Base.metadata.drop_all(bind=engine)

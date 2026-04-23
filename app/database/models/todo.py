from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Boolean, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database.base import Base
from app.database.models import PrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.database.models import User

class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Todo(Base, PrimaryKeyMixin, TimestampMixin):
    """Todo modeli."""

    __tablename__ = "todos"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    priority: Mapped[Priority] = mapped_column(
        SAEnum(Priority), default=Priority.MEDIUM, nullable=False
    )

    # Foreign key
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="todos")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Todo id={self.id} title={self.title!r}>"

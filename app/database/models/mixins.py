from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class TimestampMixin:
    """created_at va updated_at maydonlarini qo'shadi."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class PrimaryKeyMixin:
    """Auto-increment primary key qo'shadi."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


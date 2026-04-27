from sqlalchemy.orm import Session
from app.database.base import Base
from app.database.session import engine

from app.database.models import User , Todo


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    Base.metadata.drop_all(bind=engine)

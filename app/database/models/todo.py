from sqlalchemy import Column, DateTime, String, Integer, Boolean

from app.database.base import BaseModel

class TodoDB(BaseModel):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True )
    completed = Column(Boolean, nullable=True)
    deadline = Column(DateTime, nullable=True)



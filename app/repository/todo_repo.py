from app.database.models.todo import TodoDB


ModelType =


class TodoRepository(ModelType):
    def __init__(self, session):
        self.session = session

    async def create_todo(self, todo):
        todo_db = TodoDB(**todo.dict())
        self.session.add(todo_db)
        await self.session.commit()
        await self.session.refresh(todo_db)
        return todo_db

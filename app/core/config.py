from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///todo.db"
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"

    jwt_token: str = "claksdlkansdkln0-asndjansdjn0-asdasd"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

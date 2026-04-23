from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///todo.db"
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"

    jwt_token: str = "x9#Kd!2Lp@qW7mN$zR1vT8sY%uC4eB6"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

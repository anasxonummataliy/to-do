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


from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Todo App"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/todo_db"

    # JWT
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            import json

            return json.loads(v)
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

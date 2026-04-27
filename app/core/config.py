import os

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):

    db_url: str = os.getenv("DATABASE_URL")

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")


settings = Settings()

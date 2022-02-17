from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int
    redis_host: str
    redis_password: str
    redis_port: int

    class Config:
        env_file = ".env"


settings = Settings()

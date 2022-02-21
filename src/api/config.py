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
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    s3_bucket: str
    sentry_dsn: str

    class Config:
        env_file = ".env"


settings = Settings()

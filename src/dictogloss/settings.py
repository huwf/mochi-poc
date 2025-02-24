import os
from functools import lru_cache

from pydantic import computed_field, PostgresDsn, RedisDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')
    # Required fields
    ENV: str
    DB_SCHEME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: str

    # Optional fields
    DEBUG: bool = False

    @computed_field
    @property
    def db_url(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme=self.DB_SCHEME,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=f"/{self.DB_NAME}",
        )

    @computed_field
    @property
    def redis_url(self) -> RedisDsn:
        return MultiHostUrl.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=f"/{self.REDIS_DB}",
        )


@lru_cache(maxsize=1)
def get_settings():
    _env_file = os.environ.get("ENV_FILE", ".env")
    return Settings(_env_file=_env_file)

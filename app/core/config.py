from typing import Any

from pydantic import BaseSettings, PostgresDsn, validator
from vkbottle import Token


class Settings(BaseSettings):
    PORT: int = 8000

    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    MAGIC_STATS_API_LINK: str
    MAGIC_MODERS_API_LINK: str

    RCC_API_KEY: str

    RUST_BANNED_API_KEY: str

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> PostgresDsn | str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            port=values.get('POSTGRES_PORT'),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    VK_TOKEN: Token
    VK_MAGIC_HELPER_TOKEN: Token
    VERSION: str = '2.0'
    SERVER_URL: str = 'https://localhost:8000/v2/vkbot'
    SERVER_TITLE: str = 'Magic Helper VK-Bot (Test)'
    SECRET_KEY: str = 'secret'


settings = Settings()

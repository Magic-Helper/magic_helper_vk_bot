from pydantic import BaseSettings
from vkbottle import Token


class Settings(BaseSettings):
    PORT: int = 8000

    API_URL: str
    API_TOKEN: str

    VK_MAGIC_RECORDS_TOKEN: Token
    VK_MAGIC_HELPER_TOKEN: Token
    VERSION: str = '3.0'
    SECRET_KEY: str = 'secret'

    OWNER_ID: int

    HELPER_CONFIRMATION_CODE: str
    RECORD_CONFIRMATION_CODE: str


settings = Settings()

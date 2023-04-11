from pydantic import BaseSettings
from vkbottle import Token


class Settings(BaseSettings):
    PORT: int = 8000

    API_URL: str
    API_TOKEN: str

    VK_TOKEN: Token
    VK_MAGIC_HELPER_TOKEN: Token
    VERSION: str = '3.0'
    SECRET_KEY: str = 'secret'


settings = Settings()

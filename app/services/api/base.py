from app.core import settings
from app.services.api_client import APIClient


class BaseAPI:
    def __init__(self) -> None:
        self.client = APIClient(authorization_token=settings.API_TOKEN, base_url=settings.API_URL)

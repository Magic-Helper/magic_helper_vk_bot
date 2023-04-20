from app.core import settings
from app.entities import CheckInDB, CreateCheck
from app.services.api_client import APIClient


class CheckAPI:
    def __init__(self) -> None:
        self.client = APIClient(authorization_token=settings.API_TOKEN, base_url=settings.API_URL)

    async def create_check(self, steamid: str, moderator_vk_id: int, server_number: int) -> int:
        request_body = CreateCheck(steamid=steamid, moderator_vk_id=moderator_vk_id, server_number=server_number).dict(
            exclude_none=True
        )
        result = await self.client.api_POST_request('/v1/checks', body=request_body, response_model=CheckInDB)
        return result.id

    async def complete_check(self, check_id: int, is_ban: bool = False) -> CheckInDB:
        return await self.client.api_PUT_request(f'/v1/checks/{check_id}', query={'is_ban': str(is_ban)})

    async def cancel_check(self, check_id: int) -> CheckInDB:
        return await self.client.api_DELETE_request(f'/v1/checks/{check_id}')

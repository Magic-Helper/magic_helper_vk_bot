from app.entities import ModeratorProfie
from app.services.api.base import BaseAPI


class ProfileAPI(BaseAPI):
    async def get_profile_by_vk(self, vk_id: int) -> ModeratorProfie | None:
        return await self.client.api_GET_request(f'/v1/moderator/data/{vk_id}', response_model=ModeratorProfie)

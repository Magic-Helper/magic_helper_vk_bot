from app.entities import RCCPlayer
from app.services.api.base import BaseAPI


class RCCAPI(BaseAPI):
    async def get_rcc_player(self, steamid: str) -> RCCPlayer:
        return await self.client.api_GET_request(f'/v1/rcc/player/{steamid}', response_model=RCCPlayer)

    async def get_rcc_players(self, steamids: list[str]) -> list[RCCPlayer]:
        return await self.client.api_POST_request('/v1/rcc/players', body=steamids, response_model=list[RCCPlayer])

    async def give_access(self, steamid: str, moder_steamid: str | None = None) -> None:
        await self.client.api_POST_request('/v1/rcc/access', query={'steamid': steamid, 'moder_steamid': moder_steamid})

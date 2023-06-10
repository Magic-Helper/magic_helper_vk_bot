from app.entities import BanInfo, Player, PlayerStats
from app.services.api.base import BaseAPI


class MagicRustAPI(BaseAPI):
    async def get_online_players(self, load_stats: bool = False) -> list[Player]:
        return await self.client.api_GET_request(
            '/v1/magic/players/online', query={'stats': str(load_stats)}, response_model=list[Player]
        )

    async def get_online_new_players(self, days_while_new: int = 7, load_stats: bool = False) -> list[Player]:
        return await self.client.api_GET_request(
            '/v1/magic/players/online/new',
            query={'days': days_while_new, 'stats': str(load_stats)},
            response_model=list[Player],
        )

    async def get_player_stats(self, server_number: int, steamid: str) -> PlayerStats:
        return await self.client.api_GET_request(
            f'/v1/magic/server/{server_number}/stats/{steamid}', response_model=PlayerStats
        )

    async def get_banned_players(self) -> list[BanInfo]:
        return await self.client.api_GET_request('/v1/magic/players/banned', response_model=list[BanInfo])

import asyncio
from typing import TYPE_CHECKING

import pendulum
from loguru import logger
from pydantic import parse_obj_as

from app.core import constants, settings
from app.services.base_api import BaseAPI
from app.services.magic_rust.models import Player, PlayerStats

if TYPE_CHECKING:
    from app.core.typedefs import Steamid

SERVERS_ID = {
    1: 1655,
    2: 41,
    3: 39,
    4: 1930,
    5: 2011,
    6: 2098,
    7: 2342,
    8: 2343,
    9: 3558,
    10: 3771,
    11: 4265,
    12: 4663,
    13: 4721,
    14: 5088,
    15: 7773,
    16: 9096,
    17: 9097,
    18: 9360,
}


class MagicRustAPI(BaseAPI):
    """Respresents a Magic Rust API."""

    STATS_API_LINK: str = settings.MAGIC_STATS_API_LINK
    MODERS_API_LINK: str = settings.MAGIC_MODERS_API_LINK

    async def get_player_stats(self, steamid: 'Steamid', server_number: int) -> PlayerStats | None:
        """Get player stats from Magic Rust stats API.

        Args:
            steamid (Steamid): SteamID.
            server_number (int): Server number.

        Returns:
            PlayerStats: Player stats.
        """
        server_id = SERVERS_ID[server_number]
        params = {'server': server_id, 'steamid': steamid}
        method = 'getPlayerStat.php'
        response = await self.api_request(self.STATS_API_LINK, method, params=params)
        logger.debug(response)
        if response:
            return PlayerStats(**response)
        return PlayerStats(steamid=steamid)

    async def get_server_players_stats(self, server_number: int) -> list[PlayerStats]:
        """Get server players stats from Magic Rust stats API.

        Args:
            server_number (int): Server number.

        Returns:
            list[PlayerStats]: Server players stats.
        """
        server_id = SERVERS_ID[server_number]
        params = {'server': server_id}
        api_method = 'getServerPlayers_2.php'
        response = await self.api_request(self.STATS_API_LINK, api_method, params=params)
        return parse_obj_as(list[PlayerStats], response)

    async def get_online_players(self) -> list[Player]:
        """Get online players from Magic Rust moders API.

        Returns:
            list[PlayerInfo]: Online players.
        """
        api_method = 'getPlayersList.php'
        response = await self.api_request(self.MODERS_API_LINK, api_method)
        return parse_obj_as(list[Player], response)

    async def get_online_new_players(self, days: int = 7) -> list[Player]:
        """Get online new players from Magic Rust moders API.

        Args:
            days (int, optional): Days while account is defined like new. Defaults to 7.

        Returns:
            list[PlayerInfo]: Online new players.
        """
        players_online = await self.get_online_players()
        time_delta = pendulum.now(tz=constants.TIMEZONE).subtract(days=days)
        return list(filter(lambda player: player.first_join >= time_delta, players_online))

    async def get_player_stats_by_player_info(self, player_info: Player) -> list[Player]:
        """Get player stats by player info.

        Args:
            player_info (PlayerInfo): Player info.

        Returns:
            list[PlayerInfo]: Player info with stats.
        """
        player_stats = await self.get_player_stats(player_info.steamid, player_info.server_number)
        player_info.stats = player_stats
        return player_info

    async def fill_stats_for_players(self, players: list[Player]) -> list[Player]:
        """Get stats from players list.

        Args:
            players (list[PlayerInfo]): Players list.

        Returns:
            list[PlayerInfo]: Players with stats.
        """
        tasks = []
        for player in players:
            task = asyncio.ensure_future(self.get_player_stats_by_player_info(player))
            tasks.append(task)
        players = await asyncio.gather(*tasks)
        return players

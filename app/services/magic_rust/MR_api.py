import asyncio
from typing import TYPE_CHECKING

import pendulum
from loguru import logger
from pydantic import parse_obj_as

from app.core import constants, settings
from app.core.typedefs import ReportShow
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
    20: 1655,
}


class MagicRustAPI(BaseAPI):
    """Respresents a Magic Rust API."""

    STATS_API_LINK: str = settings.MAGIC_STATS_API_LINK
    MODERS_API_LINK: str = settings.MAGIC_MODERS_API_LINK

    async def api_request(  # noqa: PLR0913
        self,
        api_url: str,
        api_method: str | None = None,
        http_method: str = 'GET',
        params: dict | None = None,
        data: dict | None = None,
    ) -> dict | None:
        """Make a request to API and return JSON response.

        Args:
            api_method (str): API method.
            http_method (str, optional): HTTP method. Defaults to 'GET'.
            params (dict, optional): Parameters. Defaults to None.
            data (dict, optional): Data. Defaults to None.

        Returns:
            dict: JSON response.
        """
        if api_method:
            api_url = api_url + api_method
        return await self.request_json(api_url, http_method, params, data)

    async def get_player_stats(self, steamid: 'Steamid', server_number: int) -> PlayerStats:
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
        logger.debug('Player {steamid} stats answer: {answer}', steamid=steamid, answer=response)
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
        players = parse_obj_as(list[Player], response)
        logger.debug('Online players: {players}', players=players)
        return players

    async def get_online_players_steamids(self) -> list[int]:
        online_players = await self.get_online_players()
        return [player.steamid for player in online_players]

    async def get_online_new_players(self, days: int = 7) -> list[Player]:
        """Get online new players from Magic Rust moders API.

        Args:
            days (int, optional): Days while account is defined like new. Defaults to 7.

        Returns:
            list[PlayerInfo]: Online new players.
        """
        players_online = await self.get_online_players()
        time_delta = pendulum.now(tz=constants.TIMEZONE).subtract(days=days)
        new_players = list(filter(lambda player: player.first_join >= time_delta, players_online))
        logger.debug('Online new players: {players}', players=new_players)
        return new_players

    async def get_player_stats_by_player_info(self, player_info: Player) -> Player:
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

    async def mark_online_players_in_report(self, reports: list[ReportShow]) -> list[ReportShow]:
        online_players = await self.get_online_players()
        online_players_steamids = [player.steamid for player in online_players]
        for report in reports:
            if report.steamid in online_players_steamids:
                report.is_player_online = True
        return reports

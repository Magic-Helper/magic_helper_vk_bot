import asyncio
from typing import TYPE_CHECKING, Optional

from loguru import logger

from app.core.utils import clear_none_from_list
from app.services.RCC.RCC_api import RustCheatCheckAPI
from app.services.storage.memory_storage import RCCDataMemoryStorage

if TYPE_CHECKING:
    from app.core.typedefs import Steamid
    from app.services.RCC.models import RCCPlayer


class RCCManager:
    def __init__(self) -> None:
        self._rcc_api: RustCheatCheckAPI = RustCheatCheckAPI()
        self._rcc_data_storage: RCCDataMemoryStorage = RCCDataMemoryStorage()

    async def get_rcc_players_and_cache(self, steamids: list['Steamid']) -> list['RCCPlayer']:
        exists_steamids_info = self._rcc_data_storage.get_cached_steamids()
        exists_steamids_data = self._rcc_data_storage.get_steamids_with_data()
        new_steamids = [steamid for steamid in steamids if steamid not in exists_steamids_info]
        cached_and_online_steamids = [steamid for steamid in steamids if steamid in exists_steamids_data]

        new_rcc_players = await self._get_rcc_players(new_steamids)
        cached_rcc_players = self._rcc_data_storage.get_players(cached_and_online_steamids)

        self._cache_new_rcc_data(new_rcc_players, new_steamids)

        return new_rcc_players + cached_rcc_players

    async def _get_rcc_players(self, steamids: list['Steamid']) -> list['RCCPlayer']:
        tasks = []
        for steamid in steamids:
            task = asyncio.ensure_future(self._get_rcc_player_or_none(steamid))
            tasks.append(task)
        rcc_players = await asyncio.gather(*tasks)
        rcc_players = clear_none_from_list(rcc_players)
        return rcc_players

    async def _get_rcc_player_or_none(self, steamid: 'Steamid') -> Optional['RCCPlayer']:
        try:
            return await self._rcc_api.get_rcc_player(steamid)
        except Exception as e:
            logger.exception(e)
            return None

    def _cache_new_rcc_data(self, new_rcc_players: list['RCCPlayer'], new_steamids: list['Steamid']) -> None:
        self._rcc_data_storage.add_players(new_rcc_players)
        self._rcc_data_storage.add_cached_steamids(new_steamids)


rcc_manager = RCCManager()

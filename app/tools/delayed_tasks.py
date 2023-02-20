from typing import TYPE_CHECKING
import asyncio

from vkbottle import DelayedTask
from loguru import logger
import pendulum

from app.core import constants
from app.services.storage.memory_storage import RCCDataMemoryStorage
from app.services.magic_rust.MR_api import MagicRustAPI
from app.services.RCC.RCC_api import RustCheatCheckAPI
from app.tools import time_assistant
from app.tools.filtres import RCCPlayerFilter

if TYPE_CHECKING:
    from app.services.RCC.models import RCCPlayer


class CheckJoinedPlayersOnServer:
    def __init__(self) -> None:
        self._previous_check_players_online: set[int] | None = None
        self._mr_api = MagicRustAPI()
        self._rcc_api = RustCheatCheckAPI()
        self._rcc_filter = RCCPlayerFilter(by_seconds_passed_after_ban=60 * 60 * 24)

    async def __call__(self) -> None:
        logger.info('Checks joined players')
        online_players_steamid = await self._mr_api.get_online_players_steamids()
        joined_players = self._get_joined_players(online_players_steamid)
        self._set_new_joined_players(joined_players)
        await self._rcc_api.get_rcc_players(joined_players)  # only for cache
        # today_banned_players = self._get_today_banned_players(joined_players)

    def _get_joined_players(self, online_players_steamids: list[int]) -> list[int]:
        if self._previous_check_players_online is None:
            return online_players_steamids

        joined_players = [
            steamid for steamid in online_players_steamids if steamid not in self._previous_check_players_online
        ]
        return joined_players

    def _set_new_joined_players(self, joined_players: list[int]) -> None:
        self._previous_check_players_online = set(joined_players)

    # async def _get_today_banned_players(self, players_steamids: list[int]) -> list['RCCPlayer']:
    #     rcc_players = await self._rcc_api.get_rcc_players(players_steamids)
    #     banned_plaeyrs = self._rcc_filter.execute(rcc_players)
    #     return banned_plaeyrs


class ClearRCCCacheEveryWipe:
    def __init__(self) -> None:
        self._rcc_cache = RCCDataMemoryStorage()

    async def __call__(self) -> None:
        while True:
            await asyncio.sleep(self._seconds_to_next_wipe())
            self._rcc_cache.clear_data()

    def _seconds_to_next_wipe(self) -> int:
        next_wipe = time_assistant.get_next_wipe_day()
        time_now = pendulum.now(tz=constants.TIMEZONE)
        seconds_to_next_wipe = time_now.diff(next_wipe).in_seconds()
        logger.info(f'Seconds to next wipe {seconds_to_next_wipe}')
        return seconds_to_next_wipe


def run_delayed_tasks(loop: asyncio.AbstractEventLoop) -> None:
    for task in delayed_tasks:
        loop.create_task(task())


delayed_tasks = [
    ClearRCCCacheEveryWipe(),
    DelayedTask(seconds=constants.MINUTES_CHECKS_JOINED_PLAEYRS * 60, handler=CheckJoinedPlayersOnServer()),
]

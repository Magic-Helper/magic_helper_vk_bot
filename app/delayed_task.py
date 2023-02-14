from vkbottle import DelayedTask

from app.core import constants
from app.services.magic_rust.MR_api import MagicRustAPI
from app.tools.rcc_manager import rcc_manager


async def auto_cache_rcc_players() -> None:
    mr_api = MagicRustAPI()
    online_players_steamids = await mr_api.get_online_players_steamids()
    await rcc_manager.get_rcc_players_and_cache(online_players_steamids)


class CheckJoinedPlayersOnServer:
    def __init__(self) -> None:
        self._previous_check_players_online: set[int] | None = None
        self._interval = constants.MINUTES_CHECKS_JOINED_PLAEYRS * 60
        self._mr_api = MagicRustAPI()

    async def __call__(self) -> None:
        online_players_steamid = await self._mr_api.get_online_players_steamids()
        joined_players = self._get_joined_players(online_players_steamid)
        self._set_new_joined_plaeyrs(joined_players)

    def _get_joined_players(self, online_players: list[int]) -> list[int]:
        if self._previous_check_players_online is None:
            return online_players

        joined_players = [steamid for steamid in online_players if steamid not in self._previous_check_players_online]
        return joined_players

    def _set_new_joined_plaeyrs(self, joined_players: list[int]) -> None:
        self._previous_check_players_online = set(joined_players)


async def run_delayed_tasks() -> None:
    for task in delayed_tasks:
        await task()


delayed_tasks = [
    DelayedTask(seconds=constants.MINUTES_TO_UPDATE_RCC_CACHE, handler=auto_cache_rcc_players),
]

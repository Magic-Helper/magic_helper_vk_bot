from typing import TYPE_CHECKING

from loguru import logger

from app.services.storage.controller import ChecksStorageController

if TYPE_CHECKING:
    from app.services.magic_rust.models import Player
    from app.services.RCC.models import RCCPlayer


class PlayerFilter:
    def __init__(
        self,
        by_kd: float | None = 1.0,
        by_check_on_magic: bool = True,
    ) -> None:
        """Player filter.

        The filter is used to filter players by different parameters.
        Players can be filtered by kd, by check on magic

        Args:
            by_kd (float | None, optional): Filter by kd. Defaults to None.
            by_check_on_magic (bool, optional): Filter by check on magic. Defaults to False. If True will intialize ChecksStorageController.
        """
        self._sync_filters = []
        self._async_filters = []

        if by_kd:
            self._sync_filters.append(self._filter_by_kd)
            self.by_kd = by_kd

        if by_check_on_magic:
            self._checks_storage = ChecksStorageController()
            self._async_filters.append(self._filter_by_not_check_on_magic)
            self.by_check_on_magic = by_check_on_magic

    async def execute(self, players: list['Player']) -> list['Player']:
        """Execute filters.

        Args:
            players (list[Player]): List of players.

        Returns:
            list[Player]: List of filtered players.
        """
        return [player for player in players if await self._filter(player)]

    async def _filter(self, player: 'Player') -> bool:
        for method in self._sync_filters:
            if not method(player):
                return False

        for method in self._async_filters:
            if not await method(player):
                return False

        return True

    async def _filter_by_not_check_on_magic(self, player: 'Player') -> bool:
        """Filter by not check on magic.

        Args:
            player (Player): Player object.

        Returns:
            bool: True if player is not check on magic, False otherwise.
        """
        return not await self._checks_storage.is_player_checked(player.steamid)

    def _filter_by_kd(self, player: 'Player') -> bool:
        """Filter by kd.

        Args:
            player (Player): Player object.

        Returns:
            bool: True if player's kd is greater than self.by_kd, False otherwise.
        """
        return player.stats.kd >= self.by_kd

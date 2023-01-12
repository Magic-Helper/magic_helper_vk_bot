from typing import TYPE_CHECKING, Optional

import pendulum
from loguru import logger

from app.core import constants
from app.services.storage.check_controller import ChecksStorageController

if TYPE_CHECKING:
    from pendulum import DateTime

    from app.services.magic_rust.models import Player
    from app.services.RCC.models import RCCBan, RCCPlayer


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
            by_check_on_magic (bool, optional): Filter by check on magic. Defaults to False.
                If True will intialize ChecksStorageController.
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


class RCCPlayerFilter:
    def __init__(
        self,
        by_seconds_passed_after_ban: Optional['DateTime'] = None,
        by_check_on_magic_after_last_ban: bool = True,
        by_reason: bool = True,
    ):
        """
        RCCPlayer filter.

        The filter is used to filter RCCPlayers by different parameters.
        Players can be filtered by last ban time passed, by check on magic, by not cheat ban

        Args:
            by_seconds_passed_after_ban (DateTime, optional): Filter by last ban time passed. Defaults to None.
            by_check_on_magic_after_last_ban (bool, optional): Filter if after last ban he was checked on magic.
                Defaults to False. If True will intialize ChecksStorageController.
            by_reason (bool, optional): Filter if ban reason is 2+ 3+ or some like this. Defaults to False.
        """
        self._player_filter = []
        self._ban_filters = [self._filter_by_active_ban]

        if by_seconds_passed_after_ban:
            self._ban_filters.append(self._filter_by_last_ban_time_passed)
            self.seconds_passed_after_ban = by_seconds_passed_after_ban

        if by_check_on_magic_after_last_ban:
            self._player_filter.append(self._filter_by_not_checked_on_magic_after_last_ban)

        if by_reason:
            self._ban_filters.append(self._filter_by_reason)

    def execute(self, players: list['RCCPlayer']) -> list['RCCPlayer']:
        """Execute filters.

        Args:
            players (list[RCCPlayer]): List of players.

        Returns:
            list[RCCPlayer]: List of filtered players.
        """
        new_players = []
        for player in players:
            filtred_player = self._filter(player)
            if filtred_player:
                new_players.append(filtred_player)
        return new_players

    def _filter(self, player: 'RCCPlayer') -> Optional['RCCPlayer']:
        logger.debug(f'Filtering player {player.steamid}')
        if not player.bans:
            return None

        for method in self._player_filter:
            if not method(player):
                logger.debug(f'Player {player.steamid} was filtered by {method.__name__} method')
                return None

        filtred_player_bans = list(filter(self._filter_bans, player.bans))
        if not filtred_player_bans:
            return None
        player.bans = filtred_player_bans

        return player

    def _filter_bans(self, ban: 'RCCBan') -> bool:
        for method in self._ban_filters:
            if not method(ban):
                logger.debug(f'Player {ban} was filtered by {method.__name__} method')
                return False

        return True

    def _filter_by_not_checked_on_magic_after_last_ban(self, player: 'RCCPlayer') -> bool:
        if not player.checks:
            return True

        last_ban = max(player.bans, key=lambda ban: ban.ban_date)
        for check in player.checks:
            if check.server_name == 'MagicRust' or check.server_name == 'MAGIC RUST':
                if check.date >= last_ban.ban_date:
                    return False
        return True

    def _filter_by_last_ban_time_passed(self, ban: 'RCCBan') -> bool:
        """Filter by last ban time passed.

        Args:
            ban (RCCBan): Ban object.

        Returns:
            bool: True if ban time is greater than self.by_last_ban_time_passed, False otherwise.
        """
        available_date = pendulum.now(tz=constants.TIMEZONE).subtract(seconds=self.seconds_passed_after_ban)
        logger.debug(
            f'Filter by last ban time passed: {ban.ban_date}, {available_date}, {ban.ban_date >= available_date}'
        )
        return ban.ban_date >= available_date

    def _filter_by_reason(self, ban: 'RCCBan') -> bool:
        """Filter by reason.

        Args:
            ban (RCCBan): Ban object.

        Returns:
            bool: True if ban reason is not 2+ 3+ or some like this, False otherwise.
        """
        for part_of_available_reason in constants.AVAILABLE_BAN_REASONS:
            if (
                part_of_available_reason in ban.reason.lower()
                and ban.reason.lower() not in constants.NOT_AVAILABLE_BAN_REASONS  # noqa: W503
            ):
                return True
        logger.debug(f'Filter by reason: {ban.reason}')
        return False

    def _filter_by_active_ban(self, ban: 'RCCBan') -> bool:
        """Filter by active ban.

        Args:
            ban (RCCBan): Ban object.

        Returns:
            bool: True if ban is active, False otherwise.
        """
        logger.debug(f'Filter by active ban: {ban.active}')
        return ban.active

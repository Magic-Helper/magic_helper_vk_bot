from datetime import datetime, timedelta
from typing import Optional

from app.entities import Player
from app.tools.filtres.abc import ABCFilter


class MRPlayerFilter(ABCFilter):
    def __init__(
        self,
        *,
        kd: float = 1.0,
        check_on_magic: bool = False,
        check_on_magic_days: int = 60,
        checked_players: Optional[dict[str, int]] = None,
    ):
        if check_on_magic and checked_players is None:
            raise ValueError("checked_players can't be none if u wanna use check_on_magic filter")
        self.kd = kd
        self.check_on_magic = check_on_magic

        self._checked_players = checked_players
        self._available_time_to_not_check = (datetime.now() - timedelta(days=check_on_magic_days)).timestamp()

    def execute(self, players: list[Player]) -> list[Player]:
        return list(filter(self._filter_player, players))

    def _filter_player(self, player: Player) -> bool:
        if not self._filter_kd(player):
            return False
        if self.check_on_magic and self._is_player_checked(player):
            return False
        return True

    def _filter_kd(self, player: Player) -> bool:
        return player.stats.kd >= self.kd

    def _is_player_checked(self, player: Player) -> bool:
        if not player.steamid in self._checked_players:
            return False
        if self._checked_players[player.steamid] > self._available_time_to_not_check:
            return True
        return False

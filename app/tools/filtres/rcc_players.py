from datetime import datetime, timedelta
from typing import Optional

from app.core.constants import AVAILABLE_BAN_REASONS, NOT_AVAILABLE_BAN_REASONS
from app.entities import RCCBan, RCCPlayer
from app.tools.filtres.abc import ABCFilter


class RCCPlayersFilter(ABCFilter):
    MAGIC_RUST_NAMES = ('magicrust', 'magic rust')

    def __init__(
        self,
        *,
        seconds_passed_after_ban: Optional[float] = None,
        check_on_magic: bool = True,
        reason: bool = True,
        active_ban: bool = True,
        checked_players: Optional[dict[str, int]] = None
    ) -> None:
        if check_on_magic and checked_players is None:
            raise ValueError("checked_players can't be none if u wanna use check_on_magic filter")
        self.seconds_passed_after_ban = seconds_passed_after_ban
        self.check_on_magic = check_on_magic
        self.reason = reason
        self.active_ban = active_ban

        self._checked_players = checked_players

    def execute(self, players: list[RCCPlayer]) -> list[RCCPlayer]:
        filtred_players = []
        for player in players:
            if player.steamid is None or not player.bans:
                continue
            if self.check_on_magic and self._is_player_checked(player):
                continue
            if not self._filter_bans(player):
                continue
            filtred_players.append(player)
        return filtred_players

    def _filter_bans(self, player: RCCPlayer) -> bool:
        bans = player.bans
        if self.seconds_passed_after_ban and bans:
            available_date = (datetime.now() - timedelta(seconds=self.seconds_passed_after_ban)).timestamp()
            bans = list(filter(lambda ban: ban.ban_date >= available_date, bans))
        if self.reason and bans:
            bans = list(filter(self._reason_filter, bans))
        if self.active_ban and bans:
            bans = list(filter(lambda ban: ban.active, bans))
        if not bans:
            return False

        player.bans = bans
        return True

    def _is_player_checked(self, player: RCCPlayer) -> bool:
        last_ban: RCCBan = max(player.bans, key=lambda ban: ban.ban_date)
        if player.steamid in self._checked_players and self._checked_players[player.steamid] >= last_ban.ban_date:
            return True
        for check in player.checks:
            if check.server_name.lower in self.MAGIC_RUST_NAMES:
                if check.date >= last_ban.ban_date:
                    return True
        return False

    def _reason_filter(self, ban: RCCBan) -> bool:
        if ban.reason.lower() in NOT_AVAILABLE_BAN_REASONS:
            return False
        for available_reason in AVAILABLE_BAN_REASONS:
            if available_reason.lower() in ban.reason.lower():
                return True
        return False

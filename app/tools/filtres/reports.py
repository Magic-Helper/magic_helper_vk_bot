from datetime import datetime, timedelta

from app.entities import ReportShow
from app.tools.filtres.abc import ABCFilter


class ReportFilter(ABCFilter):
    def __init__(
        self,
        min_reports: int | None = None,
        check_on_magic: bool = False,
        banned: bool = False,
        banned_players: list[int] | None = None,
        checked_players: dict[str, int] | None = None,
        check_on_magic_days: int = 60,
    ):
        if check_on_magic and checked_players is None:
            raise ValueError("checked_players can't be none if u wanna use check_on_magic filter")
        if banned and banned_players is None:
            raise ValueError("banned can't be none if u wanna use banned_players filter")

        self.min_reports = min_reports
        self.check_on_magic = check_on_magic
        self.banned = banned

        self._banned_players = banned_players
        self._checked_players = checked_players
        self._available_time_to_not_check = (datetime.now() - timedelta(days=check_on_magic_days)).timestamp()

    def execute(self, reports: list[ReportShow]) -> list[ReportShow]:
        return list(filter(self._filter_reports, reports))

    def _filter_reports(self, report: ReportShow) -> bool:
        if self.min_reports and report.count > self.min_reports:
            return False
        if self.check_on_magic and self._is_player_checked(report.steamid):
            return False
        if self.banned and report.steamid in self._banned_players:
            return False
        return True

    def _is_player_checked(self, steamid: str) -> bool:
        if not steamid in self._checked_players:
            return False
        if self._checked_players[steamid] > self._available_time_to_not_check:
            return True
        return False

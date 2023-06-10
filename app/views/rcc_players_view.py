from datetime import datetime

from app.core import constants
from app.entities import RCCBan, RCCPlayer
from app.views import ABCUserView


class RCCPlayersView(ABCUserView):
    def __init__(self, rcc_players: list[RCCPlayer]) -> None:
        self.rcc_players = rcc_players

        self._now_time = datetime.now().timestamp()

    def render(self) -> str:
        if not self.rcc_players:
            return 'Список игрков с банами пуст'
        text = 'Игроки с банами\n'
        for player in self.rcc_players:
            bans_info = self._get_bans_info(player.bans)
            text += f'{player.steamid}: {bans_info}\n'
        return text

    def _get_bans_info(self, bans: list[RCCBan]) -> str:
        text = ''
        for ban in bans:
            after_ban_time = self._get_after_ban_time(ban)
            server_name = self._short_server_name(ban.server_name)
            text += f'{server_name}({after_ban_time})'
        return text

    def _get_after_ban_time(self, ban: RCCBan) -> str:
        time_passed = self._now_time - ban.ban_date
        return str(int(time_passed // 86400))

    def _short_server_name(self, full_server_name: str) -> str:
        lower_server_name = full_server_name.lower()
        for short_server_name in constants.RUST_SERVERS_NAME:
            if short_server_name.lower() in lower_server_name:
                return short_server_name

        if 'GLOBAL' in full_server_name:
            return full_server_name.replace('[GLOBAL]', '')[0:15]
        return full_server_name[:15]

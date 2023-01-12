from typing import TYPE_CHECKING

import pendulum

from app.core import constants

if TYPE_CHECKING:
    from app.services.RCC.models import RCCBan, RCCPlayer


class RCCPlayersView:
    def __init__(self, rcc_players: list['RCCPlayer']):
        self.rcc_players = rcc_players

    def __repr__(self) -> str:
        return self._get_rcc_players_view()

    def _get_rcc_players_view(self) -> str:
        cap_text = self._get_cap_text()
        body_text = self._get_body_text()
        text = cap_text + '\n\n' + body_text
        return text

    def _get_cap_text(self) -> str:
        return 'Список игркоов с банами: '

    def _get_body_text(self) -> str:
        body = ''
        for rcc_player in self.rcc_players:
            body += self._get_rcc_player_text(rcc_player)
        return body

    def _get_rcc_player_text(self, rcc_player: 'RCCPlayer') -> str:
        bans_text = self._get_rcc_player_bans_text(rcc_player)
        return f'{rcc_player.steamid}: {bans_text}\n'

    def _get_rcc_player_bans_text(self, rcc_player: 'RCCPlayer') -> str:
        text = ''
        for ban in rcc_player.bans:
            text += self._get_rcc_player_ban_text(ban)
        return text[:-2]

    def _get_rcc_player_ban_text(self, ban: 'RCCBan') -> str:
        after_ban_text = self._get_time_after_ban_text(ban)
        server_name_text = self._get_server_name_text(ban)
        return f'{server_name_text} - {after_ban_text}, '

    def _get_server_name_text(self, ban: 'RCCBan') -> str:
        server_name = ban.server_name
        for server in constants.RUST_SERVERS_NAME:
            if server.lower() in server_name.lower():
                return server

        if 'GLOBAL' in server_name:
            return server_name.replace('[GLOBAL]', '')[0:15]
        return server_name[:15]

    def _get_time_after_ban_text(self, ban: 'RCCBan') -> str:
        ban_date = ban.ban_date
        today = pendulum.today()
        time_after_ban = today.diff(ban_date)
        days_after_ban = time_after_ban.days
        return f'{days_after_ban} д'

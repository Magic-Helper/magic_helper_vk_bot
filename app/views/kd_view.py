from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.magic_rust.models import Player


class KDPlayersView:
    def __init__(self, players: list['Player'], kd: float):
        self.players = players
        self.kd = kd

    def __repr__(self) -> str:
        return self._get_big_kd_player_view()

    def _get_big_kd_player_view(self) -> str:
        cap_text = self._get_cap_text()
        body_text = self._get_body_text()
        text = cap_text + '\n\n' + body_text
        return text

    def _get_cap_text(self) -> str:
        return f'Игроки с кд больше {self.kd}: '

    def _get_body_text(self) -> str:
        body = ''
        for player in self.players:
            body += self._get_player_text(player)
        return body

    def _get_player_text(self, player: 'Player') -> str:
        return f'{player.steamid}: {player.stats.kills}/{player.stats.death}({player.stats.kd:.1f})\n'

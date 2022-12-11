from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.RCC.models import RCCPlayer


class RCCPlaeyrsView:
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
        return f'{rcc_player.steamid}: {len(rcc_player.bans)} банов\n'

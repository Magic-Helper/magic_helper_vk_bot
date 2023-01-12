from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.services.magic_rust.models import PlayerStats


class PlayerStatsView:
    def __init__(self, player_stats: Optional['PlayerStats']):
        self.player_stats = player_stats

    def __repr__(self) -> str:
        return self._get_player_stats_view()

    def _get_player_stats_view(self) -> str:
        if self.player_stats.nickname is None:
            return f'Для {self.player_stats.steamid} не было найдено статистики.'

        cap = self._get_cap()
        body = self._get_body()

        text = cap + '\n\n' + body
        return text

    def _get_cap(self):
        cap = f'Статистика игрока {self.player_stats.nickname}:'
        return cap

    def _get_body(self) -> str:
        body = f'Убийств: {self.player_stats.kills} ({self.player_stats.headshot})\n'
        body += f'Смертей: {self.player_stats.death}\n'
        body += f'КД: {self.player_stats.kd:.1f}'
        return body

from datetime import datetime

from app.core.constants import EMPTY_SYM
from app.core.utils import human_time
from app.entities import CheckInDB, Player, PlayerStats
from app.views import ABCUserView


class _PlayersStatsView(ABCUserView):
    KILLS_LEN = 23

    def __init__(self, players: list[Player], min_kd: float) -> None:
        self.players = players
        self.min_kd = min_kd

    def render(self) -> str:
        if not self.players:
            return 'Ничего не найдено'
        text = self.message_cap + '\n'
        for player in self.players:
            current_line = f'{player.steamid}{EMPTY_SYM} {player.stats.kd}'
            kills = f'{player.stats.kills}/{player.stats.death}\n'
            current_line += kills.rjust(self.KILLS_LEN - len(current_line) + (len(kills)), EMPTY_SYM)

            text += current_line
        print(text)
        return text

    @property
    def message_cap(self) -> str:
        ...


class NewPlayerStatsView(_PlayersStatsView):
    @property
    def message_cap(self) -> str:
        return f'Новые игроки (KD >= {self.min_kd})'


class BigKdStatsView(_PlayersStatsView):
    @property
    def message_cap(self) -> str:
        return f'Игроки с большим KD (>= {self.min_kd})'


class PlayerStatsView(ABCUserView):
    def __init__(self, player_stats: PlayerStats, player_check: CheckInDB | None = None) -> None:
        self.player_stats = player_stats
        self.player_check = player_check

    def render(self) -> str:
        if self.player_stats.nickname is None:
            return 'Для игрока не было найдено статистики.'

        return self.cap + '\n\n' + self.body

    @property
    def cap(self) -> str:
        cap = f'Статистика игрока {self.player_stats.nickname} ({self.player_stats.steamid})'
        return cap

    @property
    def body(self) -> str:
        body = f"""
Убийств {self.player_stats.kills} ({self.player_stats.headshot}) 
-- Огнестрел: {self.player_stats.kills_shot}
-- Лук/Арбалет: {self.player_stats.kills_arrow}
-- Ближний бой: {self.player_stats.kills_melee}
Смертей: {self.player_stats.death}
КД: {self.player_stats.kd:.1f}
        """
        if self.player_check:
            last_check_spend = datetime.now().timestamp() - self.player_check.start
            human_time_spend = human_time(last_check_spend)
            if self.player_check.is_ban:
                body += f'Забанен {human_time_spend} назад'
            else:
                body += f'Последняя проверка была {human_time_spend} назад'
        return body

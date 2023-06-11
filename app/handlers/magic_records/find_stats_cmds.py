from vkbottle.bot import BotLabeler, Message, rules

from app.core import patterns
from app.core.constants import DAYS_WHILE_PLAYER_NEW, MIN_STATS_FOR_NEW_PLAYER, MIN_STATS_FOR_PLAYER
from app.core.custom_rules import GetCheckAPI, GetMRAPI
from app.entities import Player
from app.services.api import CheckAPI, MagicRustAPI
from app.services.api.utils import try_get_checked_players
from app.tools.filtres import MRPlayerFilter
from app.views import BigKdStatsView, NewPlayerStatsView

stats_find_labeler = BotLabeler()
stats_find_labeler.auto_rules = [GetMRAPI(), GetCheckAPI()]


@stats_find_labeler.message(rules.VBMLRule(patterns.new_cmd))
async def get_online_new_players_with_stats(
    message: Message,
    mr_api: MagicRustAPI,
    check_api: CheckAPI,
    days: int = DAYS_WHILE_PLAYER_NEW,
    min_stats: float = MIN_STATS_FOR_NEW_PLAYER,
) -> None:
    online_players_with_stats: list[Player] = await mr_api.get_online_new_players(days_while_new=days, load_stats=True)

    checked_players = await try_get_checked_players(check_api, [player.steamid for player in online_players_with_stats])
    mr_players_filter = MRPlayerFilter(
        kd=min_stats, check_on_magic=True, checked_players=checked_players, check_on_magic_days=days + 1
    )
    filtred_players = mr_players_filter.execute(online_players_with_stats)
    sorted_players = sorted(filtred_players, key=lambda player: player.stats.kd, reverse=True)

    await message.answer(NewPlayerStatsView(sorted_players, min_kd=min_stats).render())


@stats_find_labeler.message(rules.VBMLRule(patterns.kd_cmd))
async def get_online_players_with_stats(
    message: Message,
    mr_api: MagicRustAPI,
    check_api: CheckAPI,
    min_stats: float = MIN_STATS_FOR_PLAYER,
) -> None:
    online_players_with_stats: list[Player] = await mr_api.get_online_players(load_stats=True)

    checked_players = await try_get_checked_players(check_api, [player.steamid for player in online_players_with_stats])
    mr_players_filter = MRPlayerFilter(
        kd=min_stats, check_on_magic=True, checked_players=checked_players, check_on_magic_days=180
    )
    filtred_players = mr_players_filter.execute(online_players_with_stats)
    sorted_players = sorted(filtred_players, key=lambda player: player.stats.kd, reverse=True)

    await message.answer(BigKdStatsView(sorted_players, min_kd=min_stats).render())

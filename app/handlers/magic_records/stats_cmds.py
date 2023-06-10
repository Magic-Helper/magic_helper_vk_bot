from loguru import logger
from vkbottle.bot import BotLabeler, Message, rules

from app.core import patterns
from app.core.custom_rules import GetCheckAPI, GetMRAPI
from app.entities import CheckInDB, PlayerStats
from app.services.api import CheckAPI, MagicRustAPI
from app.views import PlayerStatsView

stats_labeler = BotLabeler()
stats_labeler.auto_rules = [GetCheckAPI(), GetMRAPI()]


@stats_labeler.message(rules.VBMLRule(patterns.stats_cmd))
async def get_player_stats(
    message: Message, mr_api: MagicRustAPI, check_api: CheckAPI, server: int, steamid: str
) -> None:
    player_stats = await _try_get_player_stats(mr_api, server, steamid)
    if player_stats is None:
        return await message.reply('Произошла ошибка при попытке получить статистику.')
    last_player_check = await _try_get_last_player_check(check_api, steamid)

    return await message.answer(PlayerStatsView(player_stats, last_player_check).render())


@stats_labeler.message(rules.VBMLRule(patterns.stats_help_cmd))
async def get_player_stats_help(message: Message) -> None:
    await message.answer('Получить статистику игрока:\n/stats <server> <steamid>')


async def _try_get_player_stats(mr_api: MagicRustAPI, server: int, steamid: str) -> PlayerStats | None:
    try:
        return await mr_api.get_player_stats(server, steamid)
    except Exception as e:
        logger.exception(e)
    return None


async def _try_get_last_player_check(check_api: CheckAPI, steamid: str) -> CheckInDB | None:
    try:
        return await check_api.get_last_check(steamid)
    except Exception:
        return None

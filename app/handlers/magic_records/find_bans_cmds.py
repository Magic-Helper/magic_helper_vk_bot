from loguru import logger
from vkbottle.bot import BotLabeler, Message, rules

from app.core import patterns
from app.core.constants import DEFAULT_DAYS_PASSED_AFTER_BAN
from app.core.custom_rules.get_rules import GetCheckAPI, GetMRAPI, GetRCCAPI
from app.entities import Player, RCCPlayer
from app.services.api import RCCAPI, CheckAPI, MagicRustAPI
from app.services.api.utils import try_get_checked_players
from app.tools.filtres import RCCPlayersFilter
from app.views import RCCPlayersView

bans_find_labeler = BotLabeler()
bans_find_labeler.auto_rules = [GetMRAPI(), GetRCCAPI(), GetCheckAPI()]


@bans_find_labeler.message(rules.VBMLRule(patterns.bans_cmd))
async def get_online_players_with_bans(
    message: Message,
    rcc_api: RCCAPI,
    mr_api: MagicRustAPI,
    check_api: CheckAPI,
    days: int | None = DEFAULT_DAYS_PASSED_AFTER_BAN,
) -> None:
    online_players = await _get_online_players_or_error(mr_api, message)
    rcc_players = await _try_get_rcc_players_or_log(rcc_api, online_players)
    rcc_players_steamids = [player.steamid for player in rcc_players if player.steamid]
    checked_players_online = await try_get_checked_players(check_api, rcc_players_steamids)

    rcc_filter = RCCPlayersFilter(seconds_passed_after_ban=86400 * days, checked_players=checked_players_online)
    filtered_players = rcc_filter.execute(rcc_players)

    await message.answer(RCCPlayersView(filtered_players).render())


async def _get_online_players_or_error(mr_api: MagicRustAPI, user_message: Message) -> list[Player]:
    try:
        online_players = await mr_api.get_online_players()
    except Exception as e:
        await user_message.reply('Произошла ошибка! Не удалось загрузить игроков онлайн.')
        raise e
    else:
        return online_players


async def _try_get_rcc_players_or_log(rcc_api: RCCAPI, online_players: list[Player]) -> list[RCCPlayer]:
    players_steamids = [player.steamid for player in online_players]
    rcc_players = []
    for i in range(0, len(online_players), 20):
        try:
            rcc_players.extend(await rcc_api.get_rcc_players(players_steamids[i : i + 20]))
        except Exception as e:
            logger.exception(e)
    return rcc_players

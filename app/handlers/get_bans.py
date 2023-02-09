from typing import TYPE_CHECKING

from loguru import logger
from vkbottle.bot import BotLabeler

from app.core import constants
from app.core.exceptions import CantGetTimePassed
from app.services.magic_rust.MR_api import MagicRustAPI
from app.tools.custom_rules import CommandListRule, GetMagicRustAPIRule
from app.tools.filtres import RCCPlayerFilter
from app.tools.parser import args_parser
from app.tools.rcc_manager import rcc_manager
from app.views import RCCPlayersView

if TYPE_CHECKING:
    from vkbottle.bot import Message


get_bans_labeler = BotLabeler()


@get_bans_labeler.message(
    CommandListRule(['bans', 'баны', 'ифты'], prefixes=['/', '.'], args_count=1),
    GetMagicRustAPIRule(),
)
async def get_banned_players(
    message: 'Message',
    magic_rust_api: 'MagicRustAPI',
    args: list = None,  # type: ignore
) -> None:
    # temporary kostil'
    if args is not None and len(args) == 2:
        filter_by_active_ban = bool(args[1])
    else:
        filter_by_active_ban = False

    try:
        time_passed = args_parser.parse_time_passed(args)
    except CantGetTimePassed:
        return await message.answer('Неправильно указано время. Используйте формат 30s, 30m, 30h, 30d, 30w, 2y.')

    try:
        online_players_steamids = await _get_online_players_steamids(magic_rust_api)
    except Exception as e:
        logger.exception(e)
        return await message.answer('Ошибка при получении игроков на сервере.')

    try:
        rcc_players = await rcc_manager.get_rcc_players_and_cache(online_players_steamids)
    except Exception as e:
        logger.exception(e)
        return await message.answer('Ошибка при получении данных с RCC.')

    rcc_players_filter = RCCPlayerFilter(by_seconds_passed_after_ban=time_passed, by_active_ban=filter_by_active_ban)
    logger.debug(f'RCC players filter {rcc_players_filter}')
    filtered_rcc_players = rcc_players_filter.execute(rcc_players)
    logger.debug(f'filted rcc players: {filtered_rcc_players}')

    sorted_players = sorted(filtered_rcc_players, key=lambda player: len(player.bans), reverse=True)  # type: ignore[arg-type]

    logger.debug(f'sorted rcc players {sorted_players}')

    await message.answer(RCCPlayersView(sorted_players))


async def _get_online_players_steamids(mr_api: MagicRustAPI) -> list[int]:
    online_players = await mr_api.get_online_players()
    return [player.steamid for player in online_players]

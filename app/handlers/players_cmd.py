from typing import TYPE_CHECKING

from loguru import logger
from vkbottle.bot import BotLabeler

from app.core import constants
from app.core.utils import convert_to_seconds
from app.helpers.collector import data_collector
from app.helpers.custom_rules import (
    CommandListRule,
    GetMagicRustAPIRule,
    GetRCCDataMemoryStorageRule,
    GetRustCheatCheckAPIRule,
)
from app.helpers.filtres import PlayerFilter, RCCPlayerFilter
from app.views import NewPlayersView

if TYPE_CHECKING:
    from vkbottle.bot import Message

    from app.services.magic_rust.MR_api import MagicRustAPI
    from app.services.RCC.RCC_api import RustCheatCheckAPI
    from app.services.storage.memory_storage import RCCDataMemoryStorage


labeler = BotLabeler()


@labeler.message(
    CommandListRule(['new', 'туц', 'новые'], prefixes=['/', '.']),
    GetMagicRustAPIRule(),
)
async def get_new_players(message: 'Message', magic_rust_api: 'MagicRustAPI') -> None:
    """Handle /new command and send new players to chat"""
    new_players = await magic_rust_api.get_online_new_players()
    if not new_players:
        return await message.answer('Новых игроков не найдено')
    new_players_with_stats = await magic_rust_api.fill_stats_for_players(new_players)

    player_filter = PlayerFilter(by_kd=1.0, by_check_on_magic=True)

    filtered_players = await player_filter.execute(new_players_with_stats)
    sorted_players = sorted(filtered_players, key=lambda player: player.stats.kd, reverse=True)
    return await message.answer(NewPlayersView(sorted_players))


@labeler.message(
    CommandListRule(['bans', 'баны', 'ифты'], prefixes=['/', '.'], args_count=1),
    GetMagicRustAPIRule(),
    GetRustCheatCheckAPIRule(),
    GetRCCDataMemoryStorageRule(),
)
async def get_banned_players(
    message: 'Message',
    magic_rust_api: 'MagicRustAPI',
    rcc_api: 'RustCheatCheckAPI',
    rcc_data_storage: 'RCCDataMemoryStorage',
    args: list = None,
):
    if not args:
        time_passed = constants.LAST_BAN_TIME_PASSED
    else:
        time_passed = args[0]
    time_passed_seconds = convert_to_seconds(time_passed)

    online_players = await magic_rust_api.get_online_players()
    rcc_online_players = await data_collector.collect_rcc_data_and_caching(
        online_players, rcc_api, rcc_data_storage
    )
    logger.debug(f'Banned players collected count {len(rcc_online_players)}')

    rcc_players_filter = RCCPlayerFilter(by_seconds_passed_after_ban=time_passed_seconds)
    filtered_rcc_players = rcc_players_filter.execute(rcc_online_players)
    logger.debug(f'Banned players filtered count {len(filtered_rcc_players)}')

    sorted_players = sorted(
        filtered_rcc_players, key=lambda player: len(player.bans), reverse=True
    )

    steamids = [player.steamid for player in sorted_players]
    await message.answer(steamids)

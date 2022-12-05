from typing import TYPE_CHECKING

from eac_info import get_eac_info
from vkbottle.bot import BotLabeler

from app.helpers import filtres
from app.helpers.custom_rules import (
    CommandListRule,
    GetMagicRustAPIRule,
    GetRustCheatCheckAPIRule,
)

if TYPE_CHECKING:
    from vkbottle.bot import Message

    from app.services.magic_rust.MR_api import MagicRustAPI
    from app.services.RCC.RCC_api import RustCheatCheckAPI
labeler = BotLabeler()


@labeler.message(
    CommandListRule(['new', 'туц', 'новые'], prefixes=['/', '.']),
    GetRustCheatCheckAPIRule(),
    GetMagicRustAPIRule(),
)
async def get_new_players(
    message: 'Message', rcc_api: 'RustCheatCheckAPI', magic_rust_api: 'MagicRustAPI'
) -> None:
    """Handle /new command and send new players to chat"""
    new_players = await magic_rust_api.get_online_new_players()
    if not new_players:
        return await message.answer('Новых игроков не найдено')

    new_players_with_stats = magic_rust_api.fill_stats_for_players(new_players)
    new_players_with_stats = filtres.filter_players_by_stat(new_players_with_stats, 1.0)

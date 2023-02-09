from typing import TYPE_CHECKING

from vkbottle.bot import BotLabeler

from app.core import constants
from app.tools.custom_rules import CommandListRule, GetMagicRustAPIRule
from app.tools.filtres import PlayerFilter
from app.tools.parser import args_parser
from app.views import KDPlayersView, NewPlayersView, PlayerStatsView

if TYPE_CHECKING:
    from vkbottle.bot import Message

    from app.services.magic_rust.MR_api import MagicRustAPI


labeler = BotLabeler()


@labeler.message(
    CommandListRule(['new', 'туц', 'новые'], prefixes=['/', '.']),
    GetMagicRustAPIRule(),
)
async def get_new_players(message: 'Message', magic_rust_api: 'MagicRustAPI') -> None:
    """Handle /new command and send new players to chat"""
    new_players = await magic_rust_api.get_online_new_players(days=60)
    if not new_players:
        return await message.answer('Новых игроков не найдено')
    new_players_with_stats = await magic_rust_api.fill_stats_for_players(new_players)

    player_filter = PlayerFilter(by_kd=1, by_check_on_magic=True)

    filtered_players = await player_filter.execute(new_players_with_stats)
    sorted_players = sorted(filtered_players, key=lambda player: player.stats.kd, reverse=True)
    return await message.answer(NewPlayersView(sorted_players))


@labeler.message(CommandListRule(['kd', 'лв'], prefixes=['/', '.'], args_count=1), GetMagicRustAPIRule())
async def get_big_kd_players(message: 'Message', magic_rust_api: 'MagicRustAPI', args: list | None = None) -> None:
    if args:
        kd = float(args[0])
    else:
        kd = constants.DEFAULT_BIG_KD

    players = await magic_rust_api.get_online_players()
    players_with_stats = await magic_rust_api.fill_stats_for_players(players)

    player_filter = PlayerFilter(by_kd=kd, by_check_on_magic=True)

    filtered_players = await player_filter.execute(players_with_stats)
    sorted_players = sorted(filtered_players, key=lambda player: player.stats.kd, reverse=True)
    return await message.answer(KDPlayersView(sorted_players, kd))


@labeler.message(
    CommandListRule(['stats', 'стата', 'ыефеы'], prefixes=['/', '.'], args_count=2),
    GetMagicRustAPIRule(),
)
async def get_player_stats(
    message: 'Message',
    magic_rust_api: 'MagicRustAPI',
    args: list = None,  # type: ignore
) -> None:
    if not args or len(args) != 2:
        return await message.answer('Вывод статистики игрока.\n/stats [сервер] [steamid]')
    get_stats_args = args_parser.parse_get_stats(args)
    stats = await magic_rust_api.get_player_stats(server_number=get_stats_args.server, steamid=get_stats_args.steamid)
    await message.answer(PlayerStatsView(stats))

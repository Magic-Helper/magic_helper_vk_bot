from typing import TYPE_CHECKING, Optional

from loguru import logger
from vkbottle.bot import BotLabeler

from app.core import constants
from app.core.exceptions import UncorrectDiscord
from app.helpers import reports_message_parser
from app.helpers.custom_rules import (
    FromUserIdRule,
    GetCheckDiscordControllerRule,
    GetChecksStorageControllerRule,
    GetDiscordClientRule,
    GetOnCheckControllerRule,
    TextInMessage,
)
from app.services.discord.exceptions import DiscordTagNotFound, FriendRequestDisabled, Unauthorized

if TYPE_CHECKING:
    from vkbottle.bot import Message

    from app.core.typedefs import GetDiscord
    from app.services.discord.discord_client import DiscordClient
    from app.services.storage.check_controller import ChecksStorageController, OnCheckController
    from app.services.storage.check_discord_controller import CheckDiscordController

labeler = BotLabeler()
labeler.auto_rules = [
    FromUserIdRule(constants.VK_REPORT_GROUP_ID),
    GetOnCheckControllerRule(),
    GetCheckDiscordControllerRule(),
    GetChecksStorageControllerRule(),
]


@labeler.chat_message(TextInMessage('предоставил контакты для связи на проверку.'), GetDiscordClientRule())
async def get_discord(
    message: 'Message',
    on_check_storage: 'OnCheckController',
    discord_client: 'DiscordClient',
    check_discord_controller: 'CheckDiscordController',
    checks_storage: 'ChecksStorageController',
) -> None:
    get_discord_info = _try_get_discord_info_from_message_or_none(message)
    logger.debug(f'Discord tag: {get_discord_info}')
    if get_discord_info is None:
        return

    on_check_player_data = on_check_storage.get_on_check_data_by_nickname(get_discord_info.nickname)
    logger.debug(f'On check player data: {on_check_player_data}')
    if on_check_player_data is None:
        return

    discord_id = await try_get_discord_id_or_send_error(message, discord_client, get_discord_info)
    if discord_id is None:
        return

    logger.debug(f'Player discord id: {discord_id}')
    banned_check_ids = await check_discord_controller.get_check_ids_by_discord_id(discord_id)
    await check_discord_controller.add_discord_id(check_id=on_check_player_data.db_row, discord_id=discord_id)
    logger.debug(f'Banned check ids: {banned_check_ids}')

    # if not banned_check_ids:
    #     return await message.reply(PlayerDiscordsView(discord_id, discord_tag=get_discord_info.discord))
    # else:
    #     banned_steamids = await checks_storage.get_steamids_by_check_ids(banned_check_ids)
    #     return await message.reply(
    #         PlayerDiscordsView(discord_id, discord_tag=get_discord_info.discord, banned_steamids=banned_steamids)
    #     )


def _try_get_discord_info_from_message_or_none(message: 'Message') -> Optional['GetDiscord']:
    try:
        return reports_message_parser.parse_get_discord(message.text)
    except UncorrectDiscord:
        logger.info(f'Uncorrect discord in message {message.text}')
        return None


async def try_get_discord_id_or_send_error(
    message: 'Message', discord_client: 'DiscordClient', get_discord_info: 'GetDiscord'
) -> int | None:
    try:
        return await discord_client.get_discord_id(get_discord_info.discord)
    except Unauthorized:
        logger.critical('Discord Unauthorized')
        # message.answer(f'@{message.from_id} Нужно авторизоваться в дискорде. Перешли мне @mahryct')
    except FriendRequestDisabled:
        logger.error(f'Disabled friend request for {get_discord_info.discord}')
        # await message.reply(f'У {get_discord_info.discord} отключена возможность добавления в друзья')
        return None
    except DiscordTagNotFound:
        logger.error(f'Not found discord with tag: {get_discord_info.discord}')
        # await message.reply(f'Дискорд {get_discord_info.discord} не найден.')

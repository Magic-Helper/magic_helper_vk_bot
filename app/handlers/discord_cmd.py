from typing import TYPE_CHECKING

from loguru import logger
from vkbottle.bot import BotLabeler

from app.tools.custom_rules import CommandListRule
from app.tools.custom_rules.get_rules import GetDiscordClientRule

if TYPE_CHECKING:
    from vkbottle.bot import Message

    from app.services.discord.discord_client import DiscordClient


labeler = BotLabeler()
labeler.auto_rules = [GetDiscordClientRule()]


@labeler.message(CommandListRule(['auth', 'фгер'], prefixes=['.', '/'], args_count=1))
async def update_discord_token(message: 'Message', discord_client: 'DiscordClient', args: list = None) -> None:
    if not args:
        return await message.answer('Token required')
    token = args[0]
    discord_client.set_token(token)
    logger.info(f'Update token to {token}')
    await message.answer('Token updated')

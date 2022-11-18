from typing import TYPE_CHECKING
from vkbottle.bot import BotLabeler

from app.core.custom_rules import StorageControllersRule, CommandListRule
from app.core import args_parser

if TYPE_CHECKING:
    from vkbottle.bot import Message
    from app.services.storage.controller import ChecksStorage


labeler = BotLabeler()
labeler.auto_rules = [StorageControllersRule()]


@labeler.message(CommandListRule(['checks', 'проверки', 'сруслы'], prefixes=['/', '.']))
async def get_checks(message: Message, checks_storage: ChecksStorage):
    args = args_parser.parse_checks(message.text)
    checks = await checks_storage.get_checks(args)
    await message.answer(checks)

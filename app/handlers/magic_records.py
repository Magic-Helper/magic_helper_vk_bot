from typing import TYPE_CHECKING

from vkbottle.bot import BotLabeler

from app.core import constants
from app.tools import record_message_parser
from app.tools.custom_rules import (
    FromUserIdRule,
    GetOnCheckControllerRule,
    TextInMessage,
)

if TYPE_CHECKING:
    from vkbottle.bot import Message

    from app.services.storage.check_controller import OnCheckController

labeler = BotLabeler()
# Parse only messages from magic records group
labeler.auto_rules = [FromUserIdRule(constants.VK_RECORDS_GROUP_ID), GetOnCheckControllerRule()]


@labeler.chat_message(TextInMessage(['вызван на проверку.', '/cc2']))
async def start_check(message: 'Message', on_check_storage: 'OnCheckController') -> None:
    check_info = record_message_parser.parse_started_check(message.text)
    await on_check_storage.new_check(check_info)


@labeler.chat_message(TextInMessage('больше не проверяется.'))
async def end_check(message: 'Message', on_check_storage: 'OnCheckController') -> None:
    nickname = record_message_parser.parse_end_check(message.text)
    await on_check_storage.end_check(nickname)


@labeler.chat_message(TextInMessage('забанен с причиной'))
async def ban_check(message: 'Message', on_check_storage: 'OnCheckController') -> None:
    check_info = record_message_parser.parse_end_check(message.text)
    await on_check_storage.end_check(check_info, is_ban=True)

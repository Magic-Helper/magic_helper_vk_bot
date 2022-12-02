from typing import TYPE_CHECKING

from vkbottle.bot import BotLabeler, rules

from app.core import constants
from app.helpers import args_parser, record_message_parser
from app.helpers.custom_rules import (
    FromUserIdRule,
    MyCommandRule,
    OnCheckControllerRule,
    TextInMessage,
)

if TYPE_CHECKING:
    from vkbottle.bot import Message

    from app.services.storage.controller import OnCheckController

labeler = BotLabeler()
# Parse only messages from magic records group
labeler.auto_rules = [FromUserIdRule(constants.VK_RECORDS_GROUP_ID), OnCheckControllerRule()]


@labeler.chat_message(TextInMessage('вызван на проверку.'))
async def start_check(message: 'Message', on_check_storage: 'OnCheckController') -> None:
    check_info = record_message_parser.parse_started_check(message.text)
    await on_check_storage.new_check(check_info)


@labeler.chat_message(MyCommandRule('cc2', args_count=2))
async def stop_check(message: 'Message', on_check_storage: 'OnCheckController', args) -> None:
    check_info = args_parser.parse_cc(args)
    await on_check_storage.stoping_check(check_info.steamid)


@labeler.chat_message(MyCommandRule('cc3', args_count=2))
async def cancel_check(message: 'Message', on_check_storage: 'OnCheckController', args) -> None:
    check_info = args_parser.parse_cc(args)
    await on_check_storage.canceling_check(check_info.steamid)


@labeler.chat_message(TextInMessage('больше не проверяется.'))
async def end_check(message: 'Message', on_check_storage: 'OnCheckController') -> None:
    nickname = record_message_parser.parse_end_check(message.text)
    await on_check_storage.end_check(nickname)


@labeler.chat_message(TextInMessage('забанен с причиной'))
async def ban_check(message: 'Message', on_check_storage: 'OnCheckController') -> None:
    check_info = record_message_parser.parse_end_check(message.text)
    await on_check_storage.end_check(check_info, is_ban=True)

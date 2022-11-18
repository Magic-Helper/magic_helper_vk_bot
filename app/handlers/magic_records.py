# Обработчик сообщений от бота магик раст отчетов

from typing import TYPE_CHECKING

from vkbottle.bot import BotLabeler, rules

from app.core import constants, record_message_parser, args_parser
from app.core.custom_rules import FromUserIdRule, TextInMessage, StorageControllersRule

if TYPE_CHECKING:
    from vkbottle.bot import Message

    from app.services.storage.controller import ChecksStorage

labeler = BotLabeler()
labeler.auto_rules = [FromUserIdRule(constants.VK_RECORDS_GROUP_ID), StorageControllersRule()]


@labeler.chat_message(TextInMessage('вызван на проверку.'))
async def start_check(message: 'Message', checks_storage: 'ChecksStorage') -> None:
    check_info = record_message_parser.parse_started_check(message.text)
    await checks_storage.new_check(check_info)


@labeler.chat_message(rules.CommandRule('cc2', args_count=2))
async def stop_check(message: 'Message', checks_storage: 'ChecksStorage', args) -> None:
    check_info = args_parser.parse_cc(args)
    await checks_storage.stoping_check(check_info.steamid)


@labeler.chat_message(rules.CommandRule('cc3', args_count=2))
async def cancel_check(message: 'Message', checks_storage: 'ChecksStorage', args) -> None:
    check_info = args_parser.parse_cc(args)
    await checks_storage.canceling_check(check_info.steamid)   


@labeler.chat_message(TextInMessage('больше не проверяется.'))
async def end_check(message: 'Message', checks_storage: 'ChecksStorage') -> None:
    nickname = record_message_parser.parse_end_check(message.text)
    await checks_storage.end_check(nickname)


@labeler.chat_message(TextInMessage('забанен с причиной'))
async def ban_check(message: 'Message', checks_storage: 'ChecksStorage') -> None:
    check_info = record_message_parser.parse_end_check(message.text)
    await checks_storage.end_check(check_info, is_ban=True)





# @labeler.chat_message(SearchRegexRule(r'(?<=\nИгрок бездействует )\d+(?= секунд)'))


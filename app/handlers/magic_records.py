# Обработчик сообщений от бота магик раст отчетов

from typing import TYPE_CHECKING

from vkbottle.bot import BotLabeler, rules

from app.core import constants, record_message_parser
from app.core.typedefs import StartedCheck
from app.custom_rules import FromUserIdRule, SearchRegexRule
from app.handlers import StorageControllersRule

if TYPE_CHECKING:
    from vkbottle.bot import Message

    from app.services.storage.controller import ChecksStorage

labeler = BotLabeler()
labeler.auto_rules = [FromUserIdRule(constants.VK_RECORDS_GROUP_ID), StorageControllersRule()]


@labeler.chat_message(SearchRegexRule(r'вызван на проверку.'))
async def started_check(message: 'Message', checks_storage: 'ChecksStorage'):
    check_info = record_message_parser.parse_started_check(message.text)
    await checks_storage.new_check(check_info)

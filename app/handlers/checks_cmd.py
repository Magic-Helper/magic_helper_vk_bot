from typing import TYPE_CHECKING

from loguru import logger
from vkbottle.bot import BotLabeler

from app.tools import data_collector, time_assistant
from app.tools.custom_rules import (
    CommandListRule,
    GetChecksStorageControllerRule,
    GetVKAPIRule,
)
from app.views import CheckView

if TYPE_CHECKING:
    from vkbottle import API
    from vkbottle.bot import Message

    from app.services.storage.check_controller import ChecksStorageController


labeler = BotLabeler()
labeler.auto_rules = [GetChecksStorageControllerRule()]


@labeler.message(GetVKAPIRule(), CommandListRule(['checks', 'проверки', 'сруслы'], prefixes=['/', '.']))
async def get_checks(message: 'Message', checks_storage: 'ChecksStorageController', vk_api: 'API') -> None:
    """Handler for /checks command. Send checks count information to user."""
    current_work_time_interval = time_assistant.get_current_work_time()
    checks_data = await data_collector.collect_checks_info(current_work_time_interval, checks_storage, vk_api)
    logger.debug(f'Checks data: {checks_data}')
    await message.answer(CheckView(checks_data, current_work_time_interval))

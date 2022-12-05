from typing import TYPE_CHECKING

from vkbottle.bot import BotLabeler

from app.helpers import data_collector, time_assistant
from app.helpers.custom_rules import (
    CommandListRule,
    GetVKAPIRule,
    OnCheckControllerRule,
)
from app.views import CheckView

if TYPE_CHECKING:
    from vkbottle import API
    from vkbottle.bot import Message

    from app.core.typedefs import TimeInterval
    from app.services.storage.controller import ChecksStorageController


labeler = BotLabeler()
labeler.auto_rules = [OnCheckControllerRule()]


@labeler.message(
    GetVKAPIRule(), CommandListRule(['checks', 'проверки', 'сруслы'], prefixes=['/', '.'])
)
async def get_checks(
    message: 'Message', on_check_storage: 'ChecksStorageController', vk_api: 'API'
) -> None:
    """Handler for /checks command. Send checks count information to user."""
    current_work_time_interval = time_assistant.get_current_work_time()
    checks_data = data_collector.collect_checks_info(
        current_work_time_interval, on_check_storage, vk_api
    )
    await message.answer(CheckView(checks_data, current_work_time_interval))

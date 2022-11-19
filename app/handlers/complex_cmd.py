from typing import TYPE_CHECKING

from vkbottle.bot import BotLabeler

from app.helpers import time_assistant, data_collector
from app.helpers.custom_rules import CommandListRule, StorageControllersRule, GetVKApiRule
from app.views import CheckView

if TYPE_CHECKING:
    from vkbottle import API
    from vkbottle.bot import Message

    from app.core.typedefs import TimeInterval
    from app.services.storage.controller import ChecksStorage


labeler = BotLabeler()
labeler.auto_rules = [StorageControllersRule()]


@labeler.message(
    GetVKApiRule(), CommandListRule(['checks', 'проверки', 'сруслы'], prefixes=['/', '.'])
)
async def get_checks(message: 'Message', checks_storage: 'ChecksStorage', vk_api: 'API') -> None:
    current_work_time_interval = time_assistant.get_current_work_time()
    checks_data = data_collector.collect_checks_info(
        current_work_time_interval, checks_storage, vk_api
    )
    await message.answer(CheckView(checks_data, current_work_time_interval))

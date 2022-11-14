from typing import TYPE_CHECKING, Optional

from app.core import constants
from app.handlers.base import MagicLabeler

if TYPE_CHECKING:
    from vkbottle.bot import Message


labeler = MagicLabeler()


@labeler.chat_message(from_user=constants.VK_REPORT_GROUP_ID)

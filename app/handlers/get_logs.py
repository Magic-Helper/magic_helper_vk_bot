from typing import TYPE_CHECKING

import pendulum
from vkbottle import DocMessagesUploader
from vkbottle.bot import BotLabeler

from app.core import constants, logs
from app.tools.custom_rules.filter_rules import CommandListRule

if TYPE_CHECKING:
    from vkbottle.bot import Message


labeler = BotLabeler()


@labeler.private_message(CommandListRule(['logs', 'логи', 'дщпы'], ['.', '/'], args_count=1))
async def get_logs(message: 'Message', args: list = None) -> None:
    time_start, time_end = _parse_get_logs_args(args)
    logs_bytes = await logs.get_debug_logs_bytes_by_dates(time_start, time_end)
    logs_upload = await DocMessagesUploader(message.ctx_api).upload(
        title='debug.log', file_source=logs_bytes, peer_id=message.peer_id
    )
    await message.answer(attachment=logs_upload)


def _parse_get_logs_args(args: list | None) -> tuple[pendulum.DateTime, pendulum.DateTime]:
    if args is None:
        now_time = pendulum.now()
        return now_time, now_time
    if len(args) == 1:
        time = _get_date_from_format(args[0])
        return time, time
    else:
        first_time = _get_date_from_format(args[0])
        second_time = _get_date_from_format(args[1])
        return first_time, second_time


def _get_date_from_format(string: str) -> pendulum.DateTime:
    return pendulum.from_format(string, fmt=constants.STRING_DATE_FORMAT)

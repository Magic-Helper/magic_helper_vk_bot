from __future__ import annotations

import loguru
from loguru import logger
from vkbottle import API, DocMessagesUploader

from app.core import settings


def add_debug_file_log() -> None:
    logger.add('logs/debug.log', rotation='1 week', level='DEBUG')


def add_info_file_log() -> None:
    logger.add('logs/info.log', rotation='500mb', level='INFO')


def add_error_vk_message_log() -> None:
    logger.add(_send_error_log_to_owner, level='ERROR', enqueue=False)


async def _send_error_log_to_owner(message: loguru.Message) -> None:
    vk_api = API(token=settings.VK_MAGIC_HELPER_TOKEN)
    if message.record.get('exception'):
        await _send_exception_log(vk_api, message)
    else:
        await _send_error_log(vk_api, message)


async def _send_exception_log(vk_api: API, message: loguru.Message) -> None:
    file_name = _get_exception_file_name(message)
    text_bytes = message.encode()
    exception_doc = await DocMessagesUploader(vk_api).upload(
        title=file_name, file_source=text_bytes, peer_id=settings.OWNER_ID
    )
    await vk_api.messages.send(user_id=settings.OWNER_ID, attachment=exception_doc, random_id=0)


async def _send_error_log(vk_api: API, message: loguru.Message) -> None:
    await vk_api.messages.send(user_id=settings.OWNER_ID, message=message, random_id=0)


def _get_exception_file_name(message: loguru.Message) -> str:
    record = message.record
    module, name = record.get('module'), record.get('name')
    return 'ex_' + module + '_' + name + '.log'

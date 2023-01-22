from __future__ import annotations

from datetime import datetime

import aiofiles
import aiofiles.os
import loguru
from loguru import logger
from vkbottle import API, DocMessagesUploader

from app.core import constants, settings

__all__ = ['add_debug_file_log', 'add_error_vk_message_log']


def add_debug_file_log() -> None:
    logger.add('debug.log', rotation='500mb', level='DEBUG')


def add_error_vk_message_log() -> None:
    logger.add(send_vk_message_to_owner, level='ERROR', enqueue=False)


async def send_vk_message_to_owner(message: loguru.Message) -> None:
    vk_api = API(token=settings.VK_TOKEN)
    if message.record.get('exception'):  # type: ignore[attr-defined]
        await _send_exception_log(vk_api, message)
    else:
        await _send_error_log(vk_api, message)


async def _send_exception_log(vk_api: API, message: loguru.Message) -> None:
    file_name = _get_exception_file_name(message)
    file_bytes = await _create_get_bytes_remove_file(file_name, message)
    exception_doc = await DocMessagesUploader(vk_api).upload(
        title=file_name, file_source=file_bytes, peer_id=constants.OWNER_VK_ID
    )
    await vk_api.messages.send(user_id=constants.OWNER_VK_ID, attachment=exception_doc, random_id=0)


async def _send_error_log(vk_api: API, message: loguru.Message) -> None:
    await vk_api.messages.send(user_id=constants.OWNER_VK_ID, message=message, random_id=0)


def _get_exception_file_name(exception_message: loguru.Message) -> str:
    record: dict = exception_message.record  # type: ignore[attr-defined]
    time: datetime = record.get('time', datetime.now())
    str_time = time.strftime('%d.%m.%Y %H-%M-%S')
    return 'exception' + str_time + '.log'


async def _create_get_bytes_remove_file(file_name: str, text: str) -> bytes:
    await _create_file(file_name, text)
    file_bytes = await _get_bytes_file(file_name)
    await _remove_file(file_name)
    return file_bytes


async def _create_file(file_name: str, text: str) -> None:
    async with aiofiles.open(file_name, 'w', encoding='utf-8') as f:
        await f.write(text)


async def _get_bytes_file(file_name: str) -> bytes:
    async with aiofiles.open(file_name, 'rb') as f:
        return await f.read()


async def _remove_file(file_name: str) -> None:
    await aiofiles.os.remove(file_name)

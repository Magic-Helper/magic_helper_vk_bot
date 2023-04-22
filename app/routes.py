from aiohttp import web
from loguru import logger
from vkbottle import Bot

from app.core import constants, settings


async def magic_helper_vk_callback_handler(request: web.Request) -> web.Response:
    data = await _try_get_request_data(request)
    if _confirmation(data, constants.VK_MAGIC_HELPER.id_):
        return web.Response(text=settings.HELPER_CONFIRMATION_CODE)
    _check_secret_key(data)
    from_id = _get_from_id(data)
    if from_id not in constants.VK_MAGIC_HELPER.available_users:
        return web.Response(text='ok', status=200)
    loop = request._loop
    bot = _get_bot(request.app, constants.BotTypes.MAGIC_HELPER_BOT)
    loop.create_task(bot.process_event(data))
    return web.Response(text='ok', status=200)


async def magic_record_vk_callback_handler(request: web.Request) -> web.Response:
    data = await _try_get_request_data(request)
    if _confirmation(data, constants.VK_MAGIC_RECORDS.id_):
        return web.Response(text=settings.RECORD_CONFIRMATION_CODE)
    _check_secret_key(data)
    loop = request._loop
    bot = _get_bot(request.app, constants.BotTypes.MAGIC_RECORDS_BOT)
    loop.create_task(bot.process_event(data))
    return web.Response(text='ok', status=200)


def setup_handlers(app: web.Application) -> None:
    app.router.add_post('/bots/v3/vk/helper', magic_helper_vk_callback_handler)
    app.router.add_post('/bots/v3/vk/records', magic_record_vk_callback_handler)


async def _try_get_request_data(request: web.Request) -> dict:
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f'Error to parse event data {await request.text()}. Error: {e}')
        raise web.HTTPBadRequest() from e
    else:
        return data


def _confirmation(data: dict, group_id: int):
    if data.get('type') == 'confirmation' and data.get('group_id') == group_id:
        return True
    return False


def _check_secret_key(data: dict) -> None:
    if data.get('secret') != settings.SECRET_KEY:
        raise web.HTTPForbidden()


def _get_from_id(data: dict) -> str:
    return data.get('object', {}).get('message', {}).get('from_id')


def _get_bot(app: web.Application, bot_type: constants.BotTypes) -> Bot:
    return app[bot_type.value]

from aiohttp import web
from loguru import logger
from vkbottle import Bot

from app.core import constants, settings


async def vk_callback_handler(request: web.Request) -> web.Response:
    data = await _try_get_request_data(request)
    _check_secret_key(data)
    group_id, from_id = _get_group_and_from_ids_or_raise(data)

    loop = request.app.loop
    if group_id == constants.VK_MAGIC_RECORDS:
        bot = _get_bot(request.app, constants.BotTypes.MAGIC_RECORDS_BOT)
        loop.create_task(bot.process_event(data))
    elif group_id == constants.VK_MAGIC_HELPER.id_ and from_id in constants.VK_MAGIC_HELPER.available_users:
        bot = _get_bot(request.app, constants.BotTypes.MAGIC_HELPER_BOT)
        loop.create_task(bot.process_event(data))
    return web.Response(text='ok', status=200)


def setup_handlers(app: web.Application) -> None:
    app.router.add_post('v3/vk_bot', vk_callback_handler)


async def _try_get_request_data(request: web.Request) -> dict:
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f'Error to parse event data {await request.text()}. Error: {e}')
        raise web.HTTPBadRequest() from e
    else:
        return data


def _check_secret_key(data: dict) -> None:
    if data.get('secret') != settings.SECRET_KEY:
        raise web.HTTPForbidden()


def _get_group_and_from_ids_or_raise(data: dict) -> tuple[int, int | None]:
    group_id = data.get('group_id')
    if not (group_id and group_id in constants.GROUP_IDS):
        raise web.HTTPBadRequest()
    from_id = _get_from_id(data)
    return group_id, from_id


def _get_from_id(data: dict) -> str:
    return data.get('object', {}).get('message', {}).get('from_id')


def _get_bot(app: web.Application, bot_type: constants.BotTypes) -> Bot:
    return app[bot_type.value]

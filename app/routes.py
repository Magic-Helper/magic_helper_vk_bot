import asyncio
from typing import TYPE_CHECKING

from aiohttp import web
from loguru import logger

from app.core import constants, settings

if TYPE_CHECKING:
    from app.context import AppContext


async def handler(request: web.Request, ctx: 'AppContext') -> web.Response:
    try:
        data: dict = await request.json()
    except Exception:
        logger.error(f'Error when trying to get event data {await request.text()}')
        return web.Response(text='Nice try :)', status=403)

    if not (data.get('secret') == settings.SECRET_KEY):
        logger.debug('Bad secret key')
        return web.Response(text='Nice try :)', status=403)

    group_id = data.get('group_id')
    if group_id is None:
        logger.debug('No group_id')
        return web.Response(text='Nice try :)', status=403)

    if group_id not in constants.GROUP_IDS:
        logger.debug('Bad group_id')
        return web.Response(text='Nice try :)', status=403)

    from_id = data.get('object', {}).get('message', {}).get('from_id')  # )))))))))))))))))))))

    if group_id == constants.VK_FOR_CMD.id_:  # MAGICRUST Отчеты
        logger.debug('Got event for cmd bot')
        asyncio.get_running_loop().create_task(ctx.cmd_bot.process_event(data))

    elif (
        group_id == constants.VK_FOR_MESSAGE.id_ and from_id in constants.VK_FOR_MESSAGE.available_users
    ):  # MAGIC HELPER
        logger.debug('Got event for message bot')
        asyncio.get_running_loop().create_task(ctx.message_bot.process_event(data))

    return web.Response(text='ok', status=200)


def setup_webhook(app: web.Application, ctx: 'AppContext') -> None:
    app.router.add_post(
        '/v2/vkbot',
        wrap_handler(
            handler,
            ctx,
        ),
    )


def wrap_handler(handler, context: 'AppContext'):  # noqa
    async def wrapper(request: web.Request):  # noqa
        return await handler(request, context)

g   return wrapper

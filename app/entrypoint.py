import asyncio

from aiohttp import web
from loguru import logger
from vkbottle import Bot

from app.core import constants, settings
from app.handlers import magic_helper_labelers, magic_records_labelers
from app.routes import setup_handlers


def create_app(loop: asyncio.AbstractEventLoop) -> web.Application:
    logger.debug('Create web application...')
    app = web.Application(loop=loop)

    app[constants.BotTypes.MAGIC_RECORDS_BOT] = create_magic_records_bot()
    app[constants.BotTypes.MAGIC_HELPER_BOT] = create_magic_helper_bot()

    setup_handlers(app)
    return app


def create_magic_helper_bot() -> Bot:
    logger.debug('Create magic helper bot...')
    bot = Bot(token=settings.VK_MAGIC_HELPER_TOKEN)
    for mh_labeler in magic_helper_labelers:
        bot.labeler.load(mh_labeler)
    return bot


def create_magic_records_bot() -> Bot:
    logger.debug('Create magic records bot...')
    bot = Bot(token=settings.VK_MAGIC_RECORDS_TOKEN)
    for mr_labeler in magic_records_labelers:
        bot.labeler.load(mr_labeler)
    return bot

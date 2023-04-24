from aiohttp import web
from loguru import logger
from vkbottle import Bot, CtxStorage

from app.core import constants, middlewares, settings
from app.core.logs import add_debug_file_log, add_error_vk_message_log, add_info_file_log
from app.handlers import magic_helper_labelers, magic_records_labelers
from app.routes import setup_handlers
from app.services.api.check_api import CheckAPI
from app.tools.on_check import CheckCollector


def load_ctx_storage() -> None:
    ctx = CtxStorage()
    ctx.set('check_api', CheckAPI())
    ctx.set('on_check_contoller', CheckCollector())


def add_logs_sinks() -> None:
    add_debug_file_log()
    add_info_file_log()
    add_error_vk_message_log()


def create_app() -> web.Application:
    logger.debug('Create web application...')
    app = web.Application()

    app[constants.BotTypes.MAGIC_RECORDS_BOT.value] = create_magic_records_bot()
    app[constants.BotTypes.MAGIC_HELPER_BOT.value] = create_magic_helper_bot()

    setup_handlers(app)
    return app


def create_magic_helper_bot() -> Bot:
    logger.debug('Create magic helper bot...')
    bot = Bot(token=settings.VK_MAGIC_HELPER_TOKEN)
    bot.labeler.message_view.register_middleware(middleware=middlewares.LogMiddleware)
    for mh_labeler in magic_helper_labelers:
        bot.labeler.load(mh_labeler)
    return bot


def create_magic_records_bot() -> Bot:
    logger.debug('Create magic records bot...')
    bot = Bot(token=settings.VK_MAGIC_RECORDS_TOKEN)
    bot.labeler.message_view.register_middleware(middleware=middlewares.LogMiddleware)
    for mr_labeler in magic_records_labelers:
        bot.labeler.load(mr_labeler)
    return bot

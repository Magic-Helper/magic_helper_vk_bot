from aiohttp import web
from loguru import logger
from vkbottle import API, Bot, CtxStorage, Token
from vkbottle.bot import BotLabeler

from app.core import constants, middlewares, settings
from app.core.logs import add_debug_file_log, add_error_vk_message_log, add_info_file_log
from app.handlers import magic_helper_labelers, magic_records_labelers
from app.routes import setup_handlers
from app.services.api import RCCAPI, CheckAPI, MagicRustAPI, ProfileAPI, ReportAPI
from app.tools.on_check import CheckCollector


def load_ctx_storage() -> None:
    ctx = CtxStorage()
    ctx.set('check_api', CheckAPI())
    ctx.set('rcc_api', RCCAPI())
    ctx.set('mr_api', MagicRustAPI())
    ctx.set('check_collector', CheckCollector())
    ctx.set('report_api', ReportAPI())
    ctx.set('profile_api', ProfileAPI())
    ctx.set('record_vk_api', API(settings.VK_MAGIC_RECORDS_TOKEN))


def configure_logs() -> None:
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
    return _create_bot(settings.VK_MAGIC_HELPER_TOKEN, magic_helper_labelers)


def create_magic_records_bot() -> Bot:
    logger.debug('Create magic records bot...')
    return _create_bot(settings.VK_MAGIC_RECORDS_TOKEN, magic_records_labelers)


def _create_bot(token: Token, labelers: list[BotLabeler]) -> Bot:
    bot = Bot(token=token)
    bot.labeler.message_view.register_middleware(middleware=middlewares.PostLogMiddleware)
    _load_labelers(bot, labelers)
    return bot


def _load_labelers(bot: Bot, labelers: list[BotLabeler]) -> None:
    for labeler in labelers:
        bot.labeler.load(labeler)

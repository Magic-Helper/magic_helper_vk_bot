from aiohttp import web
from loguru import logger
from vkbottle import Bot
from vkbottle.callback import BotCallback

from app import routes
from app.context import AppContext
from app.core import settings
from app.handlers import (
    checks_cmd_labeler,
    discord_cmd_labeler,
    get_logs_labeler,
    magic_records_cmd_labeler,
    magic_records_labeler,
    magic_reports_labeler,
    other_cmd_labeler,
    owner_cmd_labeler,
    players_cmd_labeler,
)

message_bot_labelers = (
    magic_records_labeler,
    magic_reports_labeler,
)

cmd_bot_labelers = (
    checks_cmd_labeler,
    other_cmd_labeler,
    magic_records_cmd_labeler,
    players_cmd_labeler,
    owner_cmd_labeler,
    get_logs_labeler,
    discord_cmd_labeler,
)


async def create_app(cmd_bot: Bot, message_bot: Bot) -> web.Application:
    logger.debug('Creating app...')
    app = web.Application()

    ctx = AppContext()
    ctx.cmd_bot = cmd_bot
    ctx.message_bot = message_bot

    app.on_startup.append(ctx.on_startup)
    app.on_shutdown.append(ctx.on_shutdown)

    routes.setup_webhook(app, ctx)

    return app


async def create_cmd_bot() -> Bot:
    logger.debug('Creating cmd bot...')
    callback = BotCallback(url=settings.SERVER_URL, title=settings.SERVER_TITLE)
    bot = Bot(token=settings.VK_TOKEN, callback=callback)
    for custom_labeler in cmd_bot_labelers:
        bot.labeler.load(custom_labeler)
    return bot


async def create_message_bot() -> Bot:
    logger.debug('Creating message bot...')
    callback = BotCallback(url=settings.SERVER_URL, title=settings.SERVER_TITLE)
    bot = Bot(token=settings.VK_MAGIC_HELPER_TOKEN, callback=callback)
    for custom_labeler in message_bot_labelers:
        bot.labeler.load(custom_labeler)
    return bot

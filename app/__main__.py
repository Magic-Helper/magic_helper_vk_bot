import argparse
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument("--test", type=bool, default=False)

args = parser.parse_args()
if args.test:
    from dotenv import load_dotenv

    load_dotenv(".env.dev")


from aiohttp import web
from loguru import logger

from app.core import settings
from app.entrypoint import create_app, create_cmd_bot, create_message_bot
from app.services.storage import OnCheckMemoryStorage
from app.services.storage.controller import OnCheckController

# Создано просто чтобы чистилщик мусора не удалил
memory_storage = OnCheckMemoryStorage()
check_storage = OnCheckController()


event_loop = asyncio.new_event_loop()

cmd_bot = event_loop.run_until_complete(create_cmd_bot())
message_bot = event_loop.run_until_complete(create_message_bot())
app = event_loop.run_until_complete(create_app(cmd_bot, message_bot))

logger.info('Starting server...')
web.run_app(app, port=settings.PORT)

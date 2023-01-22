import argparse
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument('--test', type=bool, default=False)

args = parser.parse_args()
if args.test:
    from dotenv import load_dotenv

    load_dotenv('.env.dev')


from aiohttp import web
from loguru import logger

from app.core import settings
from app.entrypoint import create_app, create_cmd_bot, create_message_bot
from app.logs import add_debug_file_log, add_error_vk_message_log
from app.services.storage.check_controller import OnCheckController
from app.services.storage.memory_storage import (
    OnCheckMemoryStorage,
    RCCDataMemoryStorage,
)

# Создано просто чтобы чистилщик мусора не удалил, скорее всего это и не нужно
memory_storage = OnCheckMemoryStorage()
check_storage = OnCheckController()
rcc_data_storage = RCCDataMemoryStorage()


event_loop = asyncio.get_event_loop()

add_error_vk_message_log()
add_debug_file_log()


async def test():
    logger.error('пошел нахуй')


event_loop.run_until_complete(test())

cmd_bot = event_loop.run_until_complete(create_cmd_bot())
message_bot = event_loop.run_until_complete(create_message_bot())
app = event_loop.run_until_complete(create_app(cmd_bot, message_bot))

logger.info('Starting server...')
web.run_app(app, port=settings.PORT, loop=event_loop)

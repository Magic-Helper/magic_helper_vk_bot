import os

if not os.getenv('PROD'):
    from dotenv import load_dotenv

    load_dotenv('.env.dev')

import asyncio

from aiohttp import web
from loguru import logger

from app.core import settings
from app.entrypoint import create_app, load_ctx_storage

event_loop = asyncio.get_event_loop()

load_ctx_storage()
app = create_app()

logger.info('Starting web application')
web.run_app(app, port=settings.PORT, loop=event_loop)

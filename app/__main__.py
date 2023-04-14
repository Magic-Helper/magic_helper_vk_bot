import os

if not os.getenv('PROD'):
    from dotenv import load_dotenv

    load_dotenv('.env.dev')

import asyncio

from aiohttp import web
from loguru import logger

from app.core import settings
from app.entrypoint import create_app

event_loop = asyncio.get_event_loop()

app = create_app(loop=event_loop)

logger.info('Starting web application')
web.run_app(app, port=settings.PORT, loop=event_loop)

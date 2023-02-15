from asyncio import AbstractEventLoop
from typing import TYPE_CHECKING

from app.tools.delayed_tasks import run_delayed_tasks

if TYPE_CHECKING:
    from vkbottle import Bot


class AppContext:
    def __init__(self, loop: AbstractEventLoop) -> None:
        self.cmd_bot: Bot = None
        self.message_bot: Bot = None
        self.loop = loop

    async def on_startup(self, app=None) -> None:  # noqa
        run_delayed_tasks(self.loop)

    async def on_shutdown(self, app=None) -> None:  # noqa
        pass

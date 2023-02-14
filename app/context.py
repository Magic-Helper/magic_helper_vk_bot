from typing import TYPE_CHECKING

from app.delayed_task import run_delayed_tasks

if TYPE_CHECKING:
    from vkbottle import Bot


class AppContext:
    def __init__(self) -> None:
        self.cmd_bot: Bot = None
        self.message_bot: Bot = None

    async def on_startup(self, app=None) -> None:  # noqa
        await run_delayed_tasks()

    async def on_shutdown(self, app=None) -> None:  # noqa
        pass

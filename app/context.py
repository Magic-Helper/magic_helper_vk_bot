from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vkbottle import Bot


class AppContext:
    def __init__(self) -> None:
        self.cmd_bot: Bot = None
        self.message_bot: Bot = None

    async def on_startup(self, app=None) -> None:  # noqa
        pass

    async def on_shutdown(self, app=None) -> None:  # noqa
        pass

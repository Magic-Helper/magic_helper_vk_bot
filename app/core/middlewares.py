from vkbottle import BaseMiddleware
from vkbottle.bot import Message


class ClearSpaceBeforeLineMiddleware(BaseMiddleware[Message]):
    async def pre(self) -> None:
        self.event.text = self.event.text.replace(' \n', '\n')

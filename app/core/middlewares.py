from loguru import logger
from vkbottle import BaseMiddleware
from vkbottle.bot import Message


class ClearSpaceBeforeLineMiddleware(BaseMiddleware[Message]):
    async def pre(self) -> None:
        self.event.text = self.event.text.replace(' \n', '\n')


class LogMiddleware(BaseMiddleware[Message]):
    async def pre(self) -> None:
        logger.debug('Пришел ивент:', self.event)

    async def post(self) -> None:
        if not self.handlers:
            return

        msg = ''
        for handler in self.handlers:
            msg += f'Отработал {handler}. \n. Текст: {self.event.text}'
        logger.info(msg)

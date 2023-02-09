from typing import TYPE_CHECKING

from loguru import logger
from vkbottle.bot import BotLabeler

from app.services.rust_banned.rust_banned_api import get_eac_info
from app.tools.custom_rules import CommandListRule
from app.views import EacView

if TYPE_CHECKING:
    from vkbottle.bot import Message

labeler = BotLabeler()


@labeler.message(CommandListRule(['eac', 'иак', 'уфс'], prefixes=['/', '.'], args_count=1))
async def get_eac_info_(message: 'Message', args: list) -> None:
    steamid = args[0]
    try:
        eac_info = await get_eac_info(steamid)
        logger.info(f'Получена информация об аккаунте {steamid}: {eac_info}')
    except Exception as e:
        message.answer('Произошла ошибка, проверь правильность стимайди')
        raise e
    else:
        msg = EacView(eac_info)

    await message.answer(msg, dont_parse_links=True)

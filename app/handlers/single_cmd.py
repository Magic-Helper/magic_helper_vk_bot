from typing import TYPE_CHECKING

from vkbottle.bot import BotLabeler, rules
from eac_info import get_eac_info
from eac_info.exceptions import CantGetEacInfo, SteamIsNotFound

from app.core.custom_rules import CommandListRule
from app.views import EacView

if TYPE_CHECKING:
    from vkbottle.bot import Message

labeler = BotLabeler()

@labeler.message(CommandListRule(['eac', 'иак', 'уфс'], prefixes=['/', '.']))
async def eac(message: 'Message', args) -> None:
    steamid = args[0]
    try:
        eac_info = await get_eac_info(steamid)
    except SteamIsNotFound:
        msg = 'Информации об данном аккаунте не найдено, проверьте правильность данных'
    except CantGetEacInfo:
        msg = 'Не удалось получить информацию с nexus, попробуйте позже'
    else:
        msg = EacView(eac_info)
    
    await message.answer(msg)


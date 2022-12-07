from typing import TYPE_CHECKING

from eac_info import get_eac_info
from eac_info.exceptions import CantGetEacInfo, SteamIsNotFound
from vkbottle.bot import BotLabeler

from app.helpers.custom_rules import CommandListRule
from app.views import EacView

if TYPE_CHECKING:
    from vkbottle.bot import Message

labeler = BotLabeler()


@labeler.message(CommandListRule(['eac', 'иак', 'уфс'], prefixes=['/', '.'], args_count=1))
async def get_eac_info_(message: 'Message', args) -> None:
    steamid = args[0]
    try:
        eac_info = await get_eac_info(steamid)
    except SteamIsNotFound:
        msg = 'Информации об данном аккаунте не найдено, проверьте правильность данных'
    except CantGetEacInfo:
        msg = 'Не удалось получить информацию с nexus, попробуйте позже'
    else:
        msg = EacView(eac_info)

    await message.answer(msg, dont_parse_links=True)

from typing import TYPE_CHECKING

from eac_info import get_eac_info
from eac_info.exceptions import CantGetEacInfo, SteamIsNotFound
from loguru import logger
from vkbottle.bot import BotLabeler

from app.helpers.custom_rules import CommandListRule
from app.views import EacView

if TYPE_CHECKING:
    from vkbottle.bot import Message

labeler = BotLabeler()


@labeler.message(CommandListRule(['eac', 'иак', 'уфс'], prefixes=['/', '.'], args_count=1))
async def get_eac_info_(message: 'Message', args: list) -> None:
    steamid = args[0]
    return await message.answer(
        f'Из-за нестабильных ответов, лушче пользуйтесь просто сайтом: \nhttps://www.nexusonline.co.uk/bans/profile/?id={steamid}'  # noqa
    )

    try:
        eac_info = await get_eac_info(steamid)
        logger.info(f'Получена информация об аккаунте {steamid}: {eac_info}')
    except SteamIsNotFound:
        msg = 'Информации об данном аккаунте не найдено, проверьте правильность данных'
        logger.error(f'Информации об аккаунте {steamid} не найдено')
    except CantGetEacInfo:
        msg = 'Не удалось получить информацию с nexus, попробуйте позже'
        logger.error(f'Не удалось получить информацию об аккаунте {steamid}')
    else:
        msg = EacView(eac_info)

    await message.answer(msg, dont_parse_links=True)

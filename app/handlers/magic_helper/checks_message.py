from loguru import logger
from vkbottle.bot import BotLabeler, Message, rules

from app.core import constants, patterns
from app.core.custom_rules import FromUserIdRule, GetCheckAPI, GetNicknamesToSteamidStorage, GetOnCheckStorage
from app.entities import CheckStage, OnCheck
from app.services.magic_helper_api import CheckAPI
from app.tools import NicknamesToSteamidStorage, OnCheckStorage

check_msgs_labeler = BotLabeler()
check_msgs_labeler.auto_rules = [
    FromUserIdRule(constants.VK_RECORDS_GROUP_ID),
    GetCheckAPI(),
    GetNicknamesToSteamidStorage(),
    GetOnCheckStorage(),
]


@check_msgs_labeler.chat_message(rules.VBMLRule(patterns.check_start_msg))
async def start_check_message(
    message: Message,
    moder_id: int,
    nickname: str,
    server_number: int,
    steamid: str,
    check_api: CheckAPI,
    on_check_storage: OnCheckStorage,
    nicknames_to_steamid_storage: NicknamesToSteamidStorage,
) -> None:
    print(type(moder_id))
    db_row = await check_api.create_check(steamid, moder_id, server_number)
    on_check = OnCheck(
        nickname=nickname,
        db_row=db_row,
    )
    on_check_storage.set(steamid, on_check)
    nicknames_to_steamid_storage.set(nickname, steamid)


@check_msgs_labeler.chat_message(rules.VBMLRule(patterns.check_end_msg))
async def end_check_message(
    message: Message,
    nickname: str,
    check_api: CheckAPI,
    on_check_storage: OnCheckStorage,
    nicknames_to_steamid_storage: NicknamesToSteamidStorage,
) -> None:
    steamid = _get_steamid_or_raise(nicknames_to_steamid_storage, nickname)
    on_check = on_check_storage.get(steamid)
    logger.info(f'End check for {nickname}|{steamid} with stage: {on_check.stage}')
    if on_check.stage == CheckStage.STOPING:
        await check_api.complete_check(on_check.db_row)
    else:
        await check_api.cancel_check(on_check.db_row)


@check_msgs_labeler.chat_message(rules.VBMLRule(patterns.check_ban_msg))
async def ban_check_message(
    message: Message,
    nickname: str,
    check_api: CheckAPI,
    on_check_storage: OnCheckStorage,
    nicknames_to_steamid_storage: NicknamesToSteamidStorage,
) -> None:
    steamid = _get_steamid_or_raise(nicknames_to_steamid_storage, nickname)
    on_check = on_check_storage.get(steamid)
    logger.info(f'Comlete check with BAN for {nickname}|{steamid}')
    await check_api.complete_check(on_check.db_row, is_ban=True)


def _get_steamid_or_raise(nicknames_to_steamid_storage: NicknamesToSteamidStorage, nickname: str) -> str:
    steamid = nicknames_to_steamid_storage.get(nickname)
    if not steamid:
        raise TypeError(f'Steamid for {nickname} expected str, not None')
    return steamid

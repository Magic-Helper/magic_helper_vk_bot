from loguru import logger
from vkbottle.bot import BotLabeler, Message, rules

from app.core import patterns
from app.core.custom_rules import GetOnCheckStorage
from app.entities import CheckStage, OnCheck
from app.tools import OnCheckStorage

check_cmds_labeler = BotLabeler()
check_cmds_labeler.auto_rules = [
    GetOnCheckStorage(),
]


@check_cmds_labeler.chat_message(rules.VBMLRule(patterns.check_end_cmd))
async def stop_check(
    message: Message,
    steamid: str,
    on_check_storage: OnCheckStorage,
) -> None:
    _update_on_check_stage_and_save(on_check_storage, steamid, CheckStage.STOPING)


@check_cmds_labeler.chat_message(rules.VBMLRule(patterns.cancel_check_cmd))
async def cancel_check(message: Message, steamid: str, on_check_storage: OnCheckStorage) -> None:
    _update_on_check_stage_and_save(on_check_storage, steamid, CheckStage.CANCELING)


def _update_on_check_stage_and_save(on_check_storage: OnCheckStorage, steamid: int, new_stage: CheckStage) -> None:
    on_check = _get_on_check_or_raise(on_check_storage, steamid)
    on_check.stage = new_stage
    on_check_storage.set(steamid, on_check)
    logger.info(f'Update check stage for {on_check.nickname}|{steamid} at {new_stage}')


def _get_on_check_or_raise(on_check_storage: OnCheckStorage, steamid: str) -> OnCheck:
    on_check = on_check_storage.get(steamid)
    if not on_check:
        raise TypeError(f'on_check for {steamid} expected OnCheck, not None')
    return on_check

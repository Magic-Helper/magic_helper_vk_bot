from vkbottle import CtxStorage
from vkbottle.bot import BotLabeler, Message, rules

from app.core import constants
from app.entities import OnCheck
from app.tools import nickname_to_steamid_storage, on_check_storage
from app.core.custom_rules.filter_rules import FromUserIdRule
from app.core import patterns

ctx_storage = CtxStorage()

labeler = BotLabeler
labeler.auto_rules = [FromUserIdRule(constants.VK_RECORDS_GROUP_ID)]


@labeler.chat_message(rules.VBMLRule(patterns.check_start))
async def start_check_message(moder_id: int, nickname: str, server_number: int, steamid: str) -> None:
    db_row = moder_id  # Replace on db request
    on_check = OnCheck(
        nickname=nickname,
        db_row=db_row,
    )
    on_check_storage.set(steamid, on_check)
    nickname_to_steamid_storage.set(nickname, steamid)


@labeler.chat_message(rules.VBMLRule(patterns.check_end))
async def end_check_message(message: Message, moder_id: int, nickname: str) -> None:
    pass


@labeler.chat_message(rules.VBMLRule(patterns.check_ban))
async def ban_check_message(message: Message, moder_id: int, nickname: str, reason: str) -> None:
    pass

from vkbottle import API, Callback, Keyboard
from vkbottle.bot import BotLabeler, Message, rules

from app.core import constants, middlewares, patterns
from app.core.constants import VK_MAGIC_RECORDS
from app.core.custom_rules import FromUserIdRule, GetCheckCollector, GetRecordVKAPI
from app.entities.payloads import GiveCheckerAccessPayload
from app.tools.on_check import CheckCollector

check_msgs_labeler = BotLabeler()
check_msgs_labeler.message_view.register_middleware(middlewares.ClearSpaceBeforeLineMiddleware)
check_msgs_labeler.auto_rules = [
    FromUserIdRule(constants.VK_RECORDS_GROUP_ID),
    GetCheckCollector(),
]


@check_msgs_labeler.chat_message(rules.VBMLRule(patterns.check_start_msg), GetRecordVKAPI())
async def start_check_message(
    message: Message,
    moder_id: int,
    nickname: str,
    server_number: int,
    steamid: str,
    check_collector: CheckCollector,
    record_vk_api: API,
) -> None:
    await check_collector.start_check(steamid, server_number, nickname, moder_id)
    await record_vk_api.messages.edit(
        peer_id=VK_MAGIC_RECORDS.chat_peer_id,
        message=message.text,
        keyboard=_start_check_keyboard(steamid),
        conversation_message_id=message.conversation_message_id,
    )


@check_msgs_labeler.chat_message(rules.VBMLRule(patterns.check_end_msg))
async def end_check_message(
    message: Message,
    nickname: str,
    check_collector: CheckCollector,
) -> None:
    await check_collector.end_check(nickname)


@check_msgs_labeler.chat_message(rules.VBMLRule(patterns.check_ban_msg))
async def ban_check_message(
    message: Message,
    nickname: str,
    check_collector: CheckCollector,
) -> None:
    await check_collector.ban_check(nickname)


def _start_check_keyboard(steamid: int) -> str:
    return (
        Keyboard(inline=True)
        .add(Callback('Выдать доступ', GiveCheckerAccessPayload(give_checker_steamid=steamid).dict()))
        .get_json()
    )

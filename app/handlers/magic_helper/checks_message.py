from vkbottle.bot import BotLabeler, Message, rules

from app.core import constants, middlewares, patterns
from app.core.custom_rules import FromUserIdRule, GetCheckCollector
from app.tools.on_check import CheckCollector

check_msgs_labeler = BotLabeler()
check_msgs_labeler.message_view.register_middleware(middlewares.ClearSpaceBeforeLineMiddleware)
check_msgs_labeler.auto_rules = [
    FromUserIdRule(constants.VK_RECORDS_GROUP_ID),
    GetCheckCollector(),
]


@check_msgs_labeler.chat_message(rules.VBMLRule(patterns.check_start_msg))
async def start_check_message(
    message: Message,
    moder_id: int,
    nickname: str,
    server_number: int,
    steamid: str,
    check_collector: CheckCollector,
) -> None:
    await check_collector.start_check(steamid, server_number, nickname, moder_id)


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

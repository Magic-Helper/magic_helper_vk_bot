from vkbottle.bot import BotLabeler, Message, rules

from app.core import patterns
from app.core.custom_rules import GetCheckCollector
from app.entities import CheckStage
from app.tools.on_check import CheckCollector

check_cmds_labeler = BotLabeler()
check_cmds_labeler.auto_rules = [
    GetCheckCollector(),
]


@check_cmds_labeler.chat_message(rules.VBMLRule(patterns.check_end_cmd))
async def stop_check(
    message: Message,
    steamid: str,
    check_collector: CheckCollector,
) -> None:
    check_collector.change_stage(steamid, CheckStage.STOPING)


@check_cmds_labeler.chat_message(rules.VBMLRule(patterns.cancel_check_cmd))
async def cancel_check(message: Message, steamid: str, check_collector: CheckCollector) -> None:
    check_collector.change_stage(steamid, CheckStage.CANCELING)

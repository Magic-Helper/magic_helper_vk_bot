from vkbottle.bot import BotLabeler, Message, rules

from app.core import patterns
from app.core.custom_rules import GetCheckAPI, GetCheckCollector
from app.core.utils import get_work_month_interval
from app.entities import CheckStage
from app.services.api import CheckAPI
from app.tools.on_check import CheckCollector
from app.views import ModeratorChecksView

check_cmds_labeler = BotLabeler()


@check_cmds_labeler.chat_message(
    rules.VBMLRule(patterns.check_end_cmd),
    GetCheckCollector(),
)
async def stop_check(
    message: Message,
    steamid: str,
    check_collector: CheckCollector,
) -> None:
    check_collector.change_stage(steamid, CheckStage.STOPING)


@check_cmds_labeler.chat_message(
    rules.VBMLRule(patterns.cancel_check_cmd),
    GetCheckCollector(),
)
async def cancel_check(message: Message, steamid: str, check_collector: CheckCollector) -> None:
    check_collector.change_stage(steamid, CheckStage.CANCELING)


@check_cmds_labeler.message(rules.VBMLRule(patterns.checks_cmd), GetCheckAPI())
async def get_moderator_checks(message: Message, check_api: CheckAPI) -> None:
    time_start, time_end = get_work_month_interval()
    moders_checks = await check_api.get_moderator_checks(time_start=time_start, time_end=time_end)
    await message.answer(ModeratorChecksView(moders_checks).render())

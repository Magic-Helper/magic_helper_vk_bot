from vkbottle.bot import BotLabeler, Message, rules

from app.core import constants, middlewares, patterns
from app.core.custom_rules import FromUserIdRule, GetReportAPI
from app.services.api import ReportAPI

reports_msgs_labeler = BotLabeler()
reports_msgs_labeler.message_view.register_middleware(middlewares.ClearSpaceBeforeLineMiddleware)
reports_msgs_labeler.message_view.register_middleware(middlewares.CutReportMessageMiddleware)
reports_msgs_labeler.auto_rules = [
    FromUserIdRule(constants.VK_REPORT_GROUP_ID),
    GetReportAPI(),
]


@reports_msgs_labeler.message(rules.VBMLRule(patterns.report_msg))
async def report_msg_handler(
    message: Message, report_api: ReportAPI, author_nickname: str, steamid: str, server_number: int
) -> None:
    await report_api.create_report(author_nickname, steamid, server_number)

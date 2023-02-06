from typing import TYPE_CHECKING

from loguru import logger
from vkbottle.bot import BotLabeler

from app.core import constants
from app.helpers import args_parser
from app.helpers.custom_rules.filter_rules import CommandListRule
from app.helpers.custom_rules.get_rules import GetMagicRustAPIRule, GetReportControllerRule
from app.helpers.filtres import ReportsFilter
from app.views import ReportCountView, ReportsView

if TYPE_CHECKING:
    from vkbottle.bot import Message

    from app.services.magic_rust.MR_api import MagicRustAPI
    from app.services.storage.report_controller import ReportController


NewPlayersDict = dict[int, int]
OldPlayersDict = dict[int, int]

reports_cmd_labeler = BotLabeler()
reports_cmd_labeler.auto_rules = [GetReportControllerRule()]
# report_controller: ReportController


@reports_cmd_labeler.message(
    CommandListRule(['reportlist', 'кузщкедшые', 'rl', 'кд'], prefixes=['.', '/'], args_count=2), GetMagicRustAPIRule()
)
async def get_reports(
    message: 'Message', report_controller: 'ReportController', magic_rust_api: 'MagicRustAPI', args: list = None
) -> None:
    logger.debug('in get reports')
    get_reports_args = args_parser.parse_get_reports(args)
    reports = await report_controller.get_report_count_per_steamid(get_reports_args.report_start_time)
    report_filter = ReportsFilter(min_reports=get_reports_args.min_reports)
    filtred_reports = await report_filter.execute(reports)
    await message.answer(ReportsView(filtred_reports, get_report_args=get_reports_args))


@reports_cmd_labeler.message(CommandListRule(['reports', 'кузщкеы', 'r', 'к'], prefixes=['.', '/'], args_count=2))
async def get_reports_count_by_steamid(
    message: 'Message', report_controller: 'ReportController', args: list = None
) -> None:
    if args is None:
        return await message.answer(f'/reports [steamid] [time_passed={constants.DEFAULT_TIME_PASSED_AFTER_REPORT}]')
    get_reports_count_args = args_parser.parse_get_report_count(args)
    report_count = await report_controller.get_report_count_by_steamid(
        steamid=get_reports_count_args.steamid,
        start_time=get_reports_count_args.report_start_time,
    )
    await message.answer(ReportCountView(report_count=report_count, get_report_count_args=get_reports_count_args))

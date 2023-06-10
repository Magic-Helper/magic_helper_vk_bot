from vkbottle.bot import BotLabeler, Message, rules

from app.core import patterns
from app.core.constants import DEAFULT_MIN_REPORTS, HOW_DAYS_DONT_SHOW_PLAYER_IN_REPORTS
from app.core.custom_rules import GetCheckAPI, GetMRAPI, GetReportAPI
from app.entities import Player, ReportShow
from app.services.api import CheckAPI, MagicRustAPI, ReportAPI
from app.tools.filtres import ReportFilter
from app.views import ReportsView, ReportView

report_cmds_labeler = BotLabeler()
report_cmds_labeler.auto_rules = [GetReportAPI(), GetMRAPI(), GetCheckAPI()]


@report_cmds_labeler.message(rules.CommandRule('reportlist'))
async def get_reportlist(message: Message, report_api: ReportAPI, mr_api: MagicRustAPI, check_api: CheckAPI) -> None:
    time_start = message.date - 86400
    reports = await report_api.get_report_count_per_steamid(time_start)
    online_players = await mr_api.get_online_players()
    reports_show = _compile_report_show(reports, online_players)

    banned_players = await mr_api.get_banned_players()
    checked_players = await check_api.get_checked_players([report.steamid for report in reports_show])
    report_filter = ReportFilter(
        min_reports=DEAFULT_MIN_REPORTS,
        check_on_magic=True,
        banned=True,
        check_on_magic_days=HOW_DAYS_DONT_SHOW_PLAYER_IN_REPORTS,
        checked_players=checked_players,
        banned_players=banned_players,
    )
    filtered_report = report_filter.execute(reports_show)
    reports_show.sort(key=lambda report: report.count, reverse=True)
    await message.answer(ReportsView(filtered_report).render())


@report_cmds_labeler.message(rules.VBMLRule(patterns.reports_cmd))
async def get_reports(message: Message, report_api: ReportAPI, check_api: CheckAPI, steamid: str) -> None:
    time_start = message.date - 86400 * 7
    reports = await report_api.get_player_reports(steamid, time_start)
    player_check_info = await check_api.get_last_check(steamid)

    report_show = ReportShow(
        steamid=steamid,
        count=reports.count,
    )

    await message.answer(ReportView(report_show, player_check_info).render())


@report_cmds_labeler.message(rules.VBMLRule(patterns.reports_help_cmd))
async def get_reports_help(message: Message) -> None:
    await message.answer(
        """
        /reportlist - список жалоб за последний день (>=3)
        /reports <steamid> - количество жалоб за последнюю неделю у игрока
    """
    )


def _compile_report_show(reports: dict[str, int], online_players: list[Player]) -> list[ReportShow]:
    online_steamids = [player.steamid for player in online_players]
    return [
        ReportShow(
            steamid=steamid,
            count=count,
            is_online=steamid in online_steamids,
        )
        for steamid, count in reports.items()
    ]

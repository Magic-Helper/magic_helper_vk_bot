from app.core.cmd_args import GetReportCount, GetReportsArgs
from app.core.typedefs import ReportShow


class ReportsView:
    emojies = {
        'online': '🟩',
        'offline': '🟥',
    }

    def __init__(self, reports: list[ReportShow], get_report_args: GetReportsArgs):
        self.reports = reports
        self._sort_reports()

        self.report_start_time = get_report_args.report_start_time
        self.min_reports = get_report_args.min_reports

    def __repr__(self) -> str:
        return self._get_reports_view()

    def _sort_reports(self) -> None:
        self.reports = sorted(self.reports, key=lambda item: item.report_count, reverse=True)

    def _get_reports_view(self) -> str:
        cap_text = self._get_cap_text()
        body_text = self._get_body_text()
        text = cap_text + '\n\n' + body_text
        return text

    def _get_cap_text(self) -> str:
        time_start = self.report_start_time.strftime('%d.%m.%Y')
        return f'Жалобы c {time_start} на игроков (>= {self.min_reports}): '

    def _get_body_text(self) -> str:
        body = ''
        for report in self.reports:
            body += self._get_report_text(report)
        return body

    def _get_report_text(self, report: ReportShow) -> str:
        online_status_emoji = self._get_online_emoji(report)
        return f'{report.steamid}: {report.report_count} {online_status_emoji}\n'

    def _get_online_emoji(self, report: ReportShow) -> str:
        if report.is_player_online:
            return self.emojies['online']
        else:
            return self.emojies['offline']


class ReportCountView:
    def __init__(self, report_count: int, get_report_count_args: GetReportCount) -> None:
        self.report_count = report_count
        self.steamid = get_report_count_args.steamid
        self.report_start_time = get_report_count_args.report_start_time

    def __repr__(self) -> str:
        return self._get_report_count_view()

    def _get_report_count_view(self) -> str:
        text = self._get_text()
        return text

    def _get_text(self) -> str:
        time_start = self.report_start_time.strftime('%d.%m.%Y')
        return f'{self.report_count} жалоб с {time_start} у {self.steamid}'

from app.core.cmd_args import GetReportsArgs


class ReportsView:
    def __init__(self, reports: dict[int, int], get_report_args: GetReportsArgs):
        self.reports = reports
        self._sort_reports()

        self.report_start_time = get_report_args.report_start_time
        self.min_reports = get_report_args.min_reports

    def __repr__(self) -> str:
        return self._get_reports_view()

    def _sort_reports(self) -> None:
        self.reports = dict(sorted(self.reports.items(), key=lambda item: item[1], reverse=True))

    def _get_reports_view(self) -> str:
        cap_text = self._get_cap_text()
        body_text = self._get_body_text()
        text = cap_text + '\n\n' + body_text
        return text

    def _get_cap_text(self) -> str:
        time_start = self.report_start_time.strftime('%d.%m.%Y')
        return f'Количество жалоб c {time_start} на игроков (>= {self.min_reports}): '

    def _get_body_text(self) -> str:
        body = ''
        for steamid, report_count in self.reports.items():
            body += self._get_report_text(steamid, report_count)
        return body

    def _get_report_text(self, steamid: int, report_count: int) -> str:
        return f'{steamid}: {report_count}\n'

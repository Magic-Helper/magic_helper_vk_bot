from datetime import datetime

from app.core.utils import human_time
from app.entities import CheckInDB, ReportShow
from app.views.abc import ABCUserView

EMOJIES = {
    'online': '🟩',
    'offline': '🟥',
}


class ReportsView(ABCUserView):
    cap = 'Жалобы на игроков за последний день (>=3)'

    def __init__(self, reports: list[ReportShow]):
        self.reports = reports

    def render(self) -> str:
        if not self.reports:
            return 'Жалоб за последний день не найдено'
        return self.cap + '\n\n' + self.body

    @property
    def body(self) -> str:
        body = ''
        for report in self.reports:
            online_status_emoji = self._get_online_emoji(report)
            body += f'{report.steamid}: {report.count} {online_status_emoji}\n'
        return body

    def _get_online_emoji(self, report: ReportShow) -> str:
        if report.is_online:
            return EMOJIES['online']
        else:
            return EMOJIES['offline']


class ReportView(ABCUserView):
    def __init__(self, report: ReportShow, check_info: CheckInDB | None = None):
        self.report = report
        self.check_info = check_info

    def render(self) -> str:
        return self.body

    @property
    def body(self) -> str:
        body = f'{self.report.count} жалоб за последнию неделю у {self.report.steamid}'
        if self.check_info:
            last_check_spend = datetime.now().timestamp() - self.check_info.start
            human_time_spend = human_time(last_check_spend)
            if self.check_info.is_ban:
                body += f'\nЗабанен {human_time_spend} назад'
            else:
                body += f'\nПоследняя проверка была {human_time_spend} назад'
        return body

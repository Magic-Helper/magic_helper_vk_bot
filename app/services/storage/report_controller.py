from typing import TYPE_CHECKING

from loguru import logger

from app.services.storage import crud
from app.services.storage.schemas.reports import ReportsCreate
from app.services.storage.session import get_session

if TYPE_CHECKING:
    from datetime import datetime

    from app.core.typedefs import ReportMessage


class ReportController:
    async def add_report(self, report_message: 'ReportMessage') -> None:
        logger.debug(f'add report - {report_message}')
        obj_in_report_message = ReportsCreate(
            author_nickname=report_message.author_nickname,
            report_steamid=report_message.report_steamid,
            server_number=report_message.server_number,
        )
        async with get_session() as session:
            await crud.reports.create(session, obj_in=obj_in_report_message)

    async def get_report_count_per_steamid(self, start_time: datetime) -> dict[int, int]:
        async with get_session() as session:
            reports_steamids = await crud.reports.get_unique_author_and_steamid_by_time(session, time_start=start_time)
        steamid_reports_count = self._calculate_unique_steamid(reports_steamids)
        return steamid_reports_count

    def _calculate_unique_steamid(self, reports: list[int]) -> dict[int, int]:
        steamid_reports_count = {}
        for steamid in reports:
            if steamid not in steamid_reports_count:
                steamid_reports_count[steamid] = 1
            else:
                steamid_reports_count[steamid] += 1
        return steamid_reports_count

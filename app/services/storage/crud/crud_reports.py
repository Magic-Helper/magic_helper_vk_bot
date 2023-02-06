from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, select

from app.services.storage.crud.base_crud import CRUDBase
from app.services.storage.models.reports import Report
from app.services.storage.schemas.reports import (
    ReportsCreate,
    ReportsUpdate,
)

if TYPE_CHECKING:
    from sqlalchemy.engine.result import ScalarResult
    from sqlalchemy.ext.asyncio import AsyncSession


class CRUDReports(CRUDBase[Report, ReportsCreate, ReportsUpdate]):
    async def get_unique_author_and_steamid_by_time(self, session: 'AsyncSession', time_start: datetime) -> list[int]:
        query = (
            select(self.model.report_steamid)
            .where(self.model.time >= time_start)
            .group_by(self.model.report_steamid, self.model.author_nickname)
        )
        result: 'ScalarResult' = await session.scalars(query)
        return result.all()

    async def get_report_count_by_steamid(self, session: 'AsyncSession', steamid: int, time_start: datetime) -> int:
        query = select(func.count(func.distinct(self.model.author_nickname, self.model.report_steamid))).where(
            self.model.report_steamid == steamid, self.model.time >= time_start
        )
        result: 'ScalarResult' = await session.scalars(query)
        return result.first()


reports = CRUDReports(Report)

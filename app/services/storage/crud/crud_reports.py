from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import select

from app.services.storage.crud.base_crud import CRUDBase
from app.services.storage.models.reports import Report
from app.services.storage.schemas.reports import (
    ReportsCreate,
    ReportsUpdate,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class CRUDReports(CRUDBase[Report, ReportsCreate, ReportsUpdate]):
    async def get_unique_author_and_steamid_by_time(self, session: 'AsyncSession', time_start: datetime) -> list[int]:
        query = (
            select(self.model.report_steamid)
            .where(self.model.time >= time_start)
            .group_by(self.model.report_steamid, self.model.author_nickname)
        )
        result = await session.scalars(query)
        return result.all()


reports = CRUDReports(Report)

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
    pass


reports = CRUDReports(Report)

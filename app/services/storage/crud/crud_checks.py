from typing import TYPE_CHECKING

from app.services.storage.crud.base_crud import CRUDBase
from app.services.storage.models import Check
from app.services.storage.schemas import CheckCreate, CheckUpdate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class CRUDCheck(CRUDBase[Check, CheckCreate, CheckUpdate]):
    pass


check = CRUDCheck(Check)

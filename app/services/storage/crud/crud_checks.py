from typing import TYPE_CHECKING

from sqlalchemy import select, func

from app.services.storage.crud.base_crud import CRUDBase
from app.services.storage.models import Check
from app.services.storage.schemas import CheckCreate, CheckUpdate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class CRUDCheck(CRUDBase[Check, CheckCreate, CheckUpdate]):
    async def get_moder_checks_count(self, db: 'AsyncSession', moder_vk: int) -> list['Check']:
        """Get checks for moder.

        Args:
            session (AsyncSession): Database session.
            moder_vk (int): Moder vk id.

        Returns:
            list[Check]: List of checks.
        """
        query = select(self.model).where(self.model.moder_vk == moder_vk)
        result = await db.scalars(query)
        return result.

check = CRUDCheck(Check)

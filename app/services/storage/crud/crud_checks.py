from typing import TYPE_CHECKING

from loguru import logger
from sqlalchemy import func, select

from app.services.storage.crud.base_crud import CRUDBase
from app.services.storage.models import Check
from app.services.storage.schemas import CheckCreate, CheckUpdate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.core.typedefs import TimeInterval


class CRUDCheck(CRUDBase[Check, CheckCreate, CheckUpdate]):
    async def get_moder_checks(
        self, session: 'AsyncSession', moder_vk: int, time_interval: 'TimeInterval'
    ) -> list[Check]:
        """Get checks of moder in time interval.

        Args:
            session (AsyncSession): Database session.
            moder_vk (int): Moder vk id.
            time_interval (TimeInterval): Time interval.

        Returns:
            list[Check]: List of checks.
        """
        logger.debug(f'Getting checks of moder {moder_vk} in time interval {time_interval}')
        query = (
            select(Check)
            .where(Check.moder_vk == moder_vk)
            .where(Check.start_time >= time_interval.start)
            .where(Check.start_time <= time_interval.end)
        )
        return await session.scalars(query).all()

    async def get_moder_checks_count(self, db: 'AsyncSession', moder_vk: int, time_interval: 'TimeInterval') -> int:
        """Get checks for moder.

        Args:
            session (AsyncSession): Database session.
            moder_vk (int): Moder vk id.

        Returns:
            int: Checks count.
        """
        logger.debug(f'Getting checks for moder {moder_vk} in {time_interval}')
        query = select(func.count(self.model.id)).where(
            self.model.moder_vk == moder_vk,
            self.model.start_time >= time_interval.start,
            self.model.start_time <= time_interval.end,
        )
        result = await db.execute(query)
        checks_count = result.first()[0]
        logger.debug(f'Found {checks_count} checks for moder {moder_vk}')
        return checks_count

    async def get_moders(self, db: 'AsyncSession') -> list[int]:
        """Get all moders.

        Args:
            session (AsyncSession): Database session.

        Returns:
            list: List of moders.
        """
        query = select(self.model.moder_vk).distinct()
        result = await db.execute(query)
        return result.scalars().all()

    async def is_steamid_exists(self, db: 'AsyncSession', steamid: int) -> bool:
        """Check if steamid exists.

        Args:
            db (AsyncSession): Database session.
            steamid (int): Steamid.

        Returns:
            bool: True if steamid exists, False otherwise.
        """
        query = select(self.model.id).where(self.model.steamid == steamid)
        result = await db.execute(query)
        return result.first() is not None


check = CRUDCheck(Check)

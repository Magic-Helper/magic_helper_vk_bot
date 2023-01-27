from typing import TYPE_CHECKING

from sqlalchemy import select

from app.services.storage.crud.base_crud import CRUDBase
from app.services.storage.models.check_discord import CheckDiscord
from app.services.storage.schemas.check_discord import (
    CheckDiscordCreate,
    CheckDiscordUpdate,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class CRUDCheckDiscord(CRUDBase[CheckDiscord, CheckDiscordCreate, CheckDiscordUpdate]):
    async def get_check_ids_by_discord_id(self, db: 'AsyncSession', discord_id: int) -> list[int]:
        query = select(self.model.check_id).where(self.model.discord_id == discord_id)
        return (await db.scalars(query)).all()

    async def add_discord_id(self, db: 'AsyncSession', discord_id: int, check_id: int) -> None:
        check_discord = CheckDiscordCreate(check_id=check_id, discord_id=discord_id)
        await self.create(db, obj_in=check_discord)


check_discord = CRUDCheckDiscord(CheckDiscord)

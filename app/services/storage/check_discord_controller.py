from app.services.storage import crud
from app.services.storage.schemas.check_discord import CheckDiscordCreate
from app.services.storage.session import get_session


class CheckDiscordController:
    async def add_discord_id(self, check_id: int, discord_id: int) -> None:
        check_discord_obj_in = CheckDiscordCreate(check_id=check_id, discord_id=discord_id)
        async with get_session() as session:
            await crud.check_discord.create(session, obj_in=check_discord_obj_in)

    async def get_check_ids_by_discord_id(self, discord_id: int) -> list[int]:
        async with get_session() as session:
            return await crud.check_discord.get_check_ids_by_discord_id(session, discord_id)

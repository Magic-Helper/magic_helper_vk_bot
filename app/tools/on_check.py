from loguru import logger

from app.entities import CheckStage, OnCheck
from app.services.api.check_api import CheckAPI
from app.tools import NicknamesToSteamidStorage, OnCheckStorage


class CheckCollector:
    def __init__(self) -> None:
        self.nicknames_to_steamid = NicknamesToSteamidStorage()
        self.on_check = OnCheckStorage()
        self.check_api = CheckAPI()

    async def start_check(self, steamid: str, server_number: int, nickname: str, moder_id: int) -> None:
        db_row = await self.check_api.create_check(steamid, moder_id, server_number)
        on_check = OnCheck(
            nickname=nickname,
            db_row=db_row,
        )
        self.on_check.set(steamid, on_check)
        self.nicknames_to_steamid.set(nickname, steamid)
        logger.info(f'Start check for {steamid}: {on_check}')

    async def end_check(self, nickname: str) -> None:
        steamid = self._get_steamid_or_raise(nickname)
        await self.end_check_by_steamid(steamid)

    async def end_check_by_steamid(self, steamid: str) -> None:
        on_check = self.on_check.get(steamid)
        logger.info(f'End check for {on_check.nickname}|{steamid} with stage: {on_check.stage}')
        if on_check.stage == CheckStage.STOPING:
            await self.check_api.complete_check(on_check.db_row)
        else:
            await self.check_api.cancel_check(on_check.db_row)
        self._delete_data_from_storages(steamid)

    async def ban_check(self, nickname: str) -> None:
        steamid = self._get_steamid_or_raise(nickname)
        await self.ban_check_by_steamid(steamid)

    async def ban_check_by_steamid(self, steamid: str) -> None:
        on_check = self.on_check.get(steamid)
        logger.info(f'Comlete check with BAN for {on_check.nickname}|{steamid}')
        await self.check_api.complete_check(on_check.db_row, is_ban=True)
        self._delete_data_from_storages(steamid)

    def change_stage(self, steamid: str, new_stage: CheckStage) -> None:
        on_check = self.on_check.get(steamid)
        on_check.stage = new_stage
        self.on_check.set(steamid, on_check)
        logger.info(f'Update check stage for {on_check.nickname}|{steamid} at {new_stage}')

    def clear_storages(self) -> None:
        self.nicknames_to_steamid.clear()
        self.on_check.clear()

    def _delete_data_from_storages(self, steamid: str) -> None:
        on_check = self.on_check.delete(steamid)
        self.nicknames_to_steamid.delete(on_check.nickname)

    def _get_steamid_or_raise(self, nickname: str) -> str:
        steamid = self.nicknames_to_steamid.get(nickname)
        if not steamid:
            raise TypeError(f'Steamid for {nickname} expected str, not None')
        return steamid

from typing import TYPE_CHECKING

import pendulum
from loguru import logger

from app.core import constants
from app.core.typedefs import CheckStage, StageData, StartedCheck, TimeInterval
from app.core.utils import singleton
from app.services.storage import crud
from app.services.storage.memory_storage import (
    NicknamesMemoryStorage,
    StageDataMemoryStorage,
)
from app.services.storage.schemas import CheckCreate, CheckUpdate
from app.services.storage.session import get_session

if TYPE_CHECKING:
    from app.core.typedefs import Nickname, Steamid
    from app.services.storage.models import Check


@singleton
class ChecksStorage:
    def __init__(self) -> None:
        self.__stage_data_storage = StageDataMemoryStorage()
        self.__nicknames_storage = NicknamesMemoryStorage()

    async def new_check(self, check_info: StartedCheck) -> 'Check':
        """Create new check in database and in memory.

        Args:
            check_info (StartedCheck): Information about check.

        Returns:
            Check: Check object.
        """
        logger.debug(f'Creating new check in storage for {check_info.nickname}')

        # Create check in database
        obj_in = CheckCreate(
            steamid=check_info.steamid,
            moder_vk=check_info.moder_vk,
            start_time=pendulum.now(constants.TIMEZONE),
        )
        async with get_session() as session:
            check = await crud.check.create(session, obj_in=obj_in)

        # Create check info in memory
        stage_data = StageData(
            steamid=check_info.steamid,
            stage=CheckStage.PROCESS,
            db_row=check.id,
        )
        self.__stage_data_storage.update(check_info.steamid, stage_data)
        self.__nicknames_storage.update(check_info.nickname, check_info.steamid)

        return check

    async def end_check(self, nickname: 'Nickname', is_ban: bool = False) -> None:
        """Update check in database.

        Args:
            nickname (str): Nickname of player.
            is_ban (bool, optional): Is player banned?. Defaults to False.
        """
        logger.debug(f'Updating check in database for {nickname}')

        steamid = self.__nicknames_storage.pop(nickname)
        stage_data = self.__stage_data_storage.pop(steamid)

        if stage_data.stage == CheckStage.CANCELING:
            logger.debug(f'Check for {nickname} was canceled')
            return await self.delete_check(nickname)

        obj_in = CheckUpdate(
            is_ban=is_ban,
            end_time=pendulum.now(constants.TIMEZONE),
        )

        async with get_session() as session:
            check = await crud.check.get(session, id=stage_data.db_row)
            await crud.check.update(session, db_obj=check, obj_in=obj_in)

    async def delete_check(self, nickname: 'Nickname') -> None:
        """Delete check from database and from memory.

        Args:
            nickname (str): Nickname of player.
        """
        logger.debug(f'Deleting check from database and memory for {nickname}')

        steamid = self.__nicknames_storage.pop(nickname)
        stage_data = self.__stage_data_storage.pop(steamid)

        async with get_session() as session:
            await crud.check.remove(session, id=stage_data.db_row)

    def stoping_check(self, steamid: 'Steamid') -> None:
        """Update check data to stop in memory.

        Args:
            nickname (str): Nickname of player.

        """
        self.update_stage(steamid, CheckStage.STOPING)

    def canceling_check(self, steamid: 'Steamid') -> None:
        """Update check data to cancel in memory.

        Args:
            nickname (str): Nickname of player.

        """
        self.update_stage(steamid, CheckStage.CANCELING)

    def update_stage(self, steamid: 'Steamid', stage: CheckStage) -> None:
        """Update stage of check in memory.

        Args:
            steamid: Steamid of player.
            nickname (str): Nickname of player.
            stage (CheckStage): New stage of check.
        """
        logger.debug(f'Updating stage for {steamid} to {stage}')

        stage_data = self.__stage_data_storage.get(steamid)
        stage_data.stage = stage

        self.__stage_data_storage.update(steamid, stage_data)

    async def get_moder_checks_count(self, moder_vk: int, time_interval: TimeInterval):
        """Get checks for moder.

        Args:
            moder_vk (int): Moder vk id.

        Returns:
            list[Check]: List of checks.
        """
        async with get_session() as session:
            return await crud.check.get_moder_checks_count(
                session, moder_vk=moder_vk, time_interval=time_interval
            )

    async def get_moders(self, time_interval: TimeInterval) -> list[int]:
        """Get moders.

        Returns:
            list[Check]: List of checks.
        """
        async with get_session() as session:
            return await crud.check.get_moders(session, time_interval=time_interval)

    async def get_multi_checks_information(
        self, moders_vk: list[int], time_interval: TimeInterval
    ):
        """Get checks for moder.

        Args:
            moder_vk (int): Moder vk id.

        Returns:
            list[Check]: List of checks.
        """
        info = []
        async with get_session() as session:
            for moder in moders_vk:
                info.append(await crud.check.get_moder_checks_count(session, moder, time_interval))
        return info

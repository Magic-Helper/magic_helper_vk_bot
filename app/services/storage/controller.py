from typing import TYPE_CHECKING

import pendulum
from loguru import logger

from app.core import constants
from app.core.typedefs import CheckStage, StageData, StartedCheck
from app.core.utils import singleton
from app.services.storage import crud
from app.services.storage.memory_storage import CheckMemoryStorage
from app.services.storage.schemas import CheckCreate, CheckUpdate
from app.services.storage.session import session

if TYPE_CHECKING:
    from app.core.typedefs import Nickname, Steamid
    from app.services.storage.models import Check


@singleton
class ChecksStorage:
    def __init__(self) -> None:
        self.__memory_storage = CheckMemoryStorage()

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
        check = await crud.check.create(session, obj_in=obj_in)

        # Create check in memory
        stage_data = StageData(
            nickname=check_info.nickname,
            steamid=check_info.steamid,
            stage=CheckStage.PROCESS,
            db_row=check.id,
        )
        self.__memory_storage.update(check_info.steamid, check_info.nickname, stage_data)

        return check

    async def end_check(self, nickname: 'Nickname', is_ban: bool = False) -> None:
        """Update check in database.

        Args:
            nickname (str): Nickname of player.
            is_ban (bool, optional): Is player banned?. Defaults to False.
        """
        logger.debug(f'Updating check in database for {nickname}')

        stage_data = self.__memory_storage.pop(nickname)

        if stage_data.stage == CheckStage.CANCELING:
            logger.debug(f'Check for {nickname} was canceled')
            return await self.delete_check(nickname)

        obj_in = CheckUpdate(
            is_ban=is_ban,
            end_time=pendulum.now(constants.TIMEZONE),
        )

        check = await crud.check.get(session, id=stage_data.db_row)
        await crud.check.update(session, db_obj=check, obj_in=obj_in)

    async def delete_check(self, nickname: 'Nickname') -> None:
        """Delete check from database and from memory.

        Args:
            nickname (str): Nickname of player.
        """
        logger.debug(f'Deleting check from database and memory for {nickname}')

        stage_data = self.__memory_storage.pop(nickname)

        await crud.check.remove(session, id=stage_data.db_row)

    def stoping_check(self, steamid: 'Steamid') -> None:
        """Update check data to stop in memory.

        Args:
            nickname (str): Nickname of player.

        """
        nickname = self.__memory_storage.get(steamid).nickname
        self.update_stage(steamid, nickname, CheckStage.STOPING)

    def canceling_check(self, steamid: 'Steamid') -> None:
        """Update check data to cancel in memory.

        Args:
            nickname (str): Nickname of player.

        """
        nickname = self.__memory_storage.get(steamid).nickname
        self.update_stage(steamid, nickname, CheckStage.CANCELING)

    def update_stage(self, steamid: 'Steamid', nickname: 'Nickname', stage: CheckStage) -> None:
        """Update stage of check in memory.

        Args:
            steamid: Steamid of player.
            nickname (str): Nickname of player.
            stage (CheckStage): New stage of check.
        """
        logger.debug(f'Updating stage for {nickname} to {stage}')

        stage_data = self.__memory_storage.get(steamid)
        stage_data.stage = stage

        self.__memory_storage.update(steamid, nickname, stage_data)

    async def get_moder_checks(self, moder_vk: int):
        """Get checks for moder.

        Args:
            moder_vk (int): Moder vk id.

        Returns:
            list[Check]: List of checks.
        """
        return await crud.check.get_moder_checks(session, moder_vk=moder_vk)

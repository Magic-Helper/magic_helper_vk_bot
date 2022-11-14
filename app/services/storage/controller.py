from typing import TYPE_CHECKING

import pendulum
from loguru import logger

from app.core import constants
from app.core.typedefs import CheckStage, StageData, StartedCheck
from app.core.utils import singleton
from app.services.storage import MemoryStorage, crud
from app.services.storage.schemas import CheckCreate, CheckUpdate
from app.services.storage.session import session

if TYPE_CHECKING:
    from app.services.storage.models import Check


@singleton
class ChecksStorage:
    def __init__(self) -> None:
        self.__storage = MemoryStorage()

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
        stage_data = StageData(stage=CheckStage.PROCESS, db_row=check.id)
        self.__storage.update(check_info.nickname, stage_data)

        return check

    async def update_check(self, nickname: str, is_ban: bool = False):
        """Update check in database.

        Args:
            nickname (str): Nickname of player.
            is_ban (bool, optional): Is player banned?. Defaults to False.
        """
        logger.debug('Updating check in database for {nickname}')

        stage_data = self.__storage.pop(nickname)

        obj_in = CheckUpdate(
            is_ban=is_ban,
            end_time=pendulum.now(constants.TIMEZONE),
        )

        check = await crud.check.get(session, id=stage_data.db_row)
        await crud.check.update(session, db_obj=check, obj_in=obj_in)

    async def delete_check(self, nickname: str):
        """Delete check from database and from memory.

        Args:
            nickname (str): Nickname of player.
        """
        logger.debug('Deleting check from database and memory for {nickname}')

        stage_data = self.__storage.get(nickname)

        await crud.check.remove(session, id=stage_data.db_row)
        self.__storage.delete(nickname)

    def update_stage(self, nickname: str, stage: CheckStage) -> None:
        """Update stage of check in memory.

        Args:
            nickname (str): Nickname of player.
            stage (CheckStage): New stage of check.
        """
        logger.debug('Updating stage for {nickname}')

        stage_data = self.__storage.get(nickname)

        stage_data.stage = stage

        self.__storage.update(nickname, stage_data)

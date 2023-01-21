from typing import TYPE_CHECKING

import pendulum
from loguru import logger

from app.core import constants
from app.core.exceptions import DontFoundCheckByRowID
from app.core.typedefs import (
    CheckStage,
    OnCheckData,
    StartedCheck,
    TimeInterval,
)
from app.services.storage import crud
from app.services.storage.memory_storage import OnCheckMemoryStorage
from app.services.storage.schemas import CheckCreate, CheckUpdate
from app.services.storage.session import get_session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.core.typedefs import Nickname, Steamid
    from app.services.storage.models import Check


class OnCheckController:
    def __init__(self) -> None:
        self.__on_check_storage = OnCheckMemoryStorage()

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
            server_number=check_info.server,
        )
        async with get_session() as session:
            check = await crud.check.create(session, obj_in=obj_in)

        # Create check info in memory
        on_check_data = OnCheckData(
            nickname=check_info.nickname,
            stage=CheckStage.PROCESS,
            db_row=check.id,
        )
        self.__on_check_storage.set_on_check(check_info.steamid, check_info.nickname, on_check_data)
        return check

    async def end_check(self, nickname: 'Nickname', is_ban: bool = False) -> None:
        """Update check in database.

        Args:
            nickname (str): Nickname of player.
            is_ban (bool, optional): Is player banned?. Defaults to False.
        """
        logger.debug(f'Updating check in database for {nickname}')

        on_check_data = self.__on_check_storage.get_data_by_nickname(nickname)

        if on_check_data.stage == CheckStage.CANCELING:
            logger.debug(f'Check for {nickname} was canceled')
            return await self.delete_check(nickname)

        obj_in = CheckUpdate(
            is_ban=is_ban,
            end_time=pendulum.now(constants.TIMEZONE),
        )

        async with get_session() as session:
            check = await self._get_check_or_raise(session, on_check_data.db_row)
            await crud.check.update(session, db_obj=check, obj_in=obj_in)

        self.__on_check_storage.delete_on_check(nickname)

    async def delete_check(self, nickname: 'Nickname') -> None:
        """Delete check from database and from memory.

        Args:
            nickname (str): Nickname of player.
        """
        logger.debug(f'Deleting check from database and memory for {nickname}')

        on_check_data = self.__on_check_storage.get_data_by_nickname(nickname)

        async with get_session() as session:
            await crud.check.remove(session, id=on_check_data.db_row)

        self.__on_check_storage.delete_on_check(nickname)

    def stoping_check(self, steamid: 'Steamid') -> None:
        """Update check data to stop in memory.

        Args:
            steamid (int): steamid of player.

        """
        self.update_stage(steamid, CheckStage.STOPING)

    def canceling_check(self, steamid: 'Steamid') -> None:
        """Update check data to cancel in memory.

        Args:
            steamid (int): steamid of player.

        """
        self.update_stage(steamid, CheckStage.CANCELING)

    def update_stage(self, steamid: 'Steamid', stage: CheckStage) -> None:
        """Update stage of check in memory.

        Args:
            steamid: Steamid of player.
            stage (CheckStage): New stage of check.
        """
        logger.debug(f'Updating stage for {steamid} to {stage}')

        self.__on_check_storage.change_state(steamid, stage)

    def get_on_check_data_by_nickname(self, nickname: 'Nickname') -> OnCheckData | None:
        """Get steamid by nickname."""
        return self.__on_check_storage.get_data_by_nickname(nickname)

    async def _get_check_or_raise(self, session: 'AsyncSession', db_row: int) -> Check:
        check = await crud.check.get(session, id=db_row)
        if not check:
            raise DontFoundCheckByRowID
        return check


class ChecksStorageController:
    """Represents controller for checks storage.

    Methods:
        get_moder_checks_count(moder_vk: int, time_interval: TimeInterval) -> list[Check]
            Returns checks for moder.
        get_moders(time_interval: TimeInterval) -> list[int]
            Returns moders.
        get_multi_checks_information(moders_vk: list[int], time_interval: TimeInterval) -> list[Check]
            Returns checks for moders.

    """

    async def get_moder_checks_count(self, moder_vk: int, time_interval: TimeInterval) -> int:
        """Get checks for moder.

        Args:
            moder_vk (int): Moder vk id.

        Returns:
            list[Check]: List of checks.
        """
        async with get_session() as session:
            return await crud.check.get_moder_checks_count(session, moder_vk=moder_vk, time_interval=time_interval)

    async def get_moders(self) -> list[int]:
        """Get moders.

        Returns:
            list[Check]: List of checks.
        """
        async with get_session() as session:
            return await crud.check.get_moders(session)

    async def get_multi_checks_information(self, moders_vk: list[int], time_interval: TimeInterval) -> list[int]:
        """Get checks for moder.

        Args:
            moder_vk (int): Moder vk id.

        Returns:
            list[int]: List of checks.
        """
        info = []
        async with get_session() as session:
            for moder in moders_vk:
                info.append(await crud.check.get_moder_checks_count(session, moder, time_interval))
        return info

    async def is_player_checked(self, steamid: 'Steamid') -> bool:
        """Check is player is already was checked.

        Args:
            steamid (int): Steamid of player.

        Returns:
            bool: is player is already was checked
        """
        async with get_session() as session:
            return await crud.check.is_steamid_exists(session, steamid)

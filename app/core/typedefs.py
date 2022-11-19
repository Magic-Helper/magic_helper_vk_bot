from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias

Steamid: TypeAlias = int
Nickname: TypeAlias = str


class CheckStage(Enum):
    """Enum for check stages"""

    PROCESS = 1
    STOPING = 2
    CANCELING = 3


@dataclass
class StageData:
    nickname: Nickname
    steamid: Steamid
    db_row: int
    stage: CheckStage


@dataclass
class PlayerData:
    nickname: Nickname = None


@dataclass
class StartedCheck:
    """Dataclass for started check information.

    Args:
        moder_vk (int): A moderator's VK ID.
        nickname (str): A nickname of a player.
        server (int): A server ID.
        steamid (int): A SteamID of a player.
    """

    nickname: str
    steamid: int
    server: int
    moder_vk: int

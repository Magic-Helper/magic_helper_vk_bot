from dataclasses import dataclass
from enum import Enum


class CheckStage(Enum):
    """Enum for check stages"""

    PROCESS = 1
    ENDED = 2
    CANCELLED = 3


@dataclass
class StageData:
    db_row: int
    stage: CheckStage


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

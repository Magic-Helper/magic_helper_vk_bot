from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from pendulum import DateTime

Steamid: TypeAlias = int
Nickname: TypeAlias = str


class CheckStage(Enum):
    """Enum for check stages"""

    PROCESS = 1
    STOPING = 2
    CANCELING = 3


@dataclass
class TimeInterval:
    """Dataclass for time interval"""

    start: 'DateTime'
    end: 'DateTime'

    def __repr__(self) -> str:
        return f'{self.start} - {self.end}'


@dataclass
class OnCheckData:
    nickname: Nickname
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


@dataclass
class Moderator:
    vk_id: int
    name: str
    surname: str

    def __repr__(self) -> str:
        return f'{self.name} {self.surname}'


@dataclass
class ModerChecksInformation:
    """Dataclass for moderator's checks information.

    Args:
        moderator (Moderator): A moderator.
        checks_count (int): A count of checks.
    """

    moderator: Moderator
    checks_count: int

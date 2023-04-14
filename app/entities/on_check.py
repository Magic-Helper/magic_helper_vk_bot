from dataclasses import dataclass
from enum import Enum


class CheckStage(Enum):
    PROCESS = 1
    STOPING = 2
    CANCELING = 3


@dataclass
class OnCheck:
    nickname: str
    db_row: int
    stage: CheckStage = CheckStage.PROCESS

from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from datetime import datetime


class CheckBase(BaseModel):
    steamid: int
    moder_vk: int
    start_time: 'datetime'
    end_time: Optional['datetime'] = None
    server_number: int | None = None
    is_ban: bool = False


class CheckCreate(CheckBase):
    pass


class CheckUpdate(CheckBase):
    steamid: int | None = None
    moder_vk: int | None = None
    start_time: Optional['datetime'] = None


class CheckInDBBase(CheckBase):
    id: int

    class Config:
        orm_mode = True


class Check(CheckInDBBase):
    pass


class CheckInDB(CheckInDBBase):
    pass

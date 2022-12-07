from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CheckBase(BaseModel):
    steamid: int
    moder_vk: int
    start_time: datetime
    end_time: Optional[datetime] = None
    server_number: int | None = None
    is_ban: bool = False


class CheckCreate(CheckBase):
    pass


class CheckUpdate(CheckBase):
    steamid: int | None = None
    moder_vk: int | None = None
    start_time: Optional[datetime] = None


class CheckInDBBase(CheckBase):
    id: int

    class Config:
        orm_mode = True


class Check(CheckInDBBase):
    pass


class CheckInDB(CheckInDBBase):
    pass

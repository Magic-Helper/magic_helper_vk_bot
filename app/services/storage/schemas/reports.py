from datetime import datetime

from pydantic import BaseModel


class ReportsBase(BaseModel):
    author_nickname: str
    report_steamid: int
    time: datetime
    server_number: int | None = None


class ReportsCreate(ReportsBase):
    pass


class ReportsUpdate(ReportsBase):
    author_nickname: str | None = None
    report_steamid: str | None = None
    time: datetime | None = None
    server_number: int | None = None


class ReportsInDBBase(ReportsBase):
    id: int

    class Config:
        orm_mode = True


class Reports(ReportsInDBBase):
    pass

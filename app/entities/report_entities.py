from pydantic import BaseModel


class CreateReport(BaseModel):
    author_nickname: str
    report_steamid: str
    server_number: int


class ReportCount(BaseModel):
    steamid: str
    count: int


class ReportShow(BaseModel):
    steamid: str
    count: int
    is_online: bool = False

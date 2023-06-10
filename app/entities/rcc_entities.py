from enum import Enum

from pydantic import BaseModel, Field


class RCCResponseStatus(Enum):
    """RCC response status enum."""

    SUCCESS = 'success'
    ERROR = 'error'


class RCCBaseResponse(BaseModel):
    status: RCCResponseStatus
    error_message: str | None = Field(None, alias='errorreason')


class RCCCheck(BaseModel):
    moder_steamid: str = Field(0, alias='moderSteamID')
    date: int = Field(0, alias='time')
    server_name: str | None = Field(None, alias='serverName')


class RCCBan(BaseModel):
    ban_id: int | None = Field(None, alias='banID')
    reason: str
    server_name: str = Field('Без названия', alias='serverName')
    OVH_server_id: int = Field(0, alias='OVHServerID')
    ban_date: int = Field(..., alias='banDate')
    unban_date: int = Field(0, alias='unbanDate')
    active: bool


class RCCPlayer(RCCBaseResponse):
    steamid: str | None = None
    checks_count: int = Field(0, alias='rcc_checks')
    checks: list[RCCCheck] | None = Field(None, alias='last_check')
    another_accs: list[str] | None = None
    bans: list[RCCBan] | None = None
    last_ips: list[str] | None = Field(None, alias='last_ip')
    last_nick: str | None = None


class BanInfo(BaseModel):
    banID: int
    nickname: str
    steamid: str
    reason: str
    time: int

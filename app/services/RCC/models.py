from enum import Enum

from pendulum import DateTime
from pydantic import BaseModel, Field, validator

from app.core.typedefs import Steamid
from app.services.validators import get_datetime_object


class RCCResponseStatus(Enum):
    """RCC response status enum."""

    SUCCESS = 'success'
    ERROR = 'error'


class RCCBaseResponse(BaseModel):
    status: RCCResponseStatus
    error_message: str | None = Field(None, alias='errorreason')


class RCCCheck(BaseModel):
    moder_steamid: Steamid
    date: DateTime = Field(0, alias='time')
    server_name: str | None = None

    # validators
    _get_datetime_object = validator('date', pre=True, allow_reuse=True)(
        get_datetime_object,
    )


class RCCBan(BaseModel):
    ban_id: int | None = Field(None, alias='banID')
    reason: str
    server_name: str = Field('Без названия', alias='serverName')
    OVH_server_id: int = Field(0, alias='OVHServerID')
    ban_date: DateTime = Field(..., alias='banDate')
    unban_date: DateTime | int = Field(0, alias='unbanDate')
    active: bool

    # validators
    _get_datetime_object = validator('ban_date', 'unban_date', pre=True, allow_reuse=True)(
        get_datetime_object,
    )


class RCCPlayer(BaseModel):
    steamid: Steamid
    checks_count: int = Field(0, alias='rcc_checks')
    checks: list[RCCCheck] | None = None
    another_accs: list[Steamid] | None = None
    bans: list[RCCBan] | None = None
    last_ips: list[str] | None = Field(None, alias='last_ip')
    last_nick: str | None = None

from typing import Optional

from pendulum import DateTime
from pydantic import BaseModel, Field, root_validator, validator

from app.core.validators import get_datetime_object


class PlayerStats(BaseModel):
    steamid: int
    kills: int = Field(0, alias='kp_total')
    death: int = Field(0, alias='d_player')
    headshot: int = Field(0, alias='kp_head')
    kd: float
    nickname: str = Field(None, alias='name')

    @root_validator(pre=True)
    def get_kd(cls, values: dict) -> dict:
        if values.get('d_player') == 0:
            values['kd'] = 0
        else:
            values['kd'] = values.get('kp_total', 0) / values.get('d_player', 1)
        return values


class Player(BaseModel):
    steamid: int = Field(..., alias='id')
    ip: str
    nickname: str
    server_number: int = Field(..., alias='server')
    first_join: DateTime = Field(..., alias='firstjoin')
    vk: Optional[int] = None
    stats: Optional[PlayerStats] = None

    # validators
    _get_datetime_object = validator('first_join', pre=True, allow_reuse=True)(
        get_datetime_object,
    )

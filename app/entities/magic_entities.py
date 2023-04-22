from pydantic import BaseModel, Field


class PlayerStats(BaseModel):
    steamid: str | None = None
    kills: int = Field(0, alias='kp_total')
    kills_arrow = Field(0, alias='kp_arrow')
    kills_shot = Field(0, alias='kp_shot')
    kills_melee = Field(0, alias='kp_melee')
    death: int = Field(0, alias='d_player')
    headshot: int = Field(0, alias='kp_head')
    kd: float
    nickname: str = Field(None, alias='name')


class Player(BaseModel):
    steamid: str = Field(..., alias='id')
    ip: str
    nickname: str
    server_number: int = Field(..., alias='server')
    first_join: int = Field(..., alias='firstjoin')
    vk: int | None = None
    stats: PlayerStats | None = None

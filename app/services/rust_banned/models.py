from pydantic import BaseModel, Field


class RustBannedResponse(BaseModel):
    steamid: int = Field(..., alias='steamid64')
    twitter_url: str | None = Field(None, alias='url')
    days_ago: int | None = None
    is_banned: bool = Field(..., alias='eac_ban_count')

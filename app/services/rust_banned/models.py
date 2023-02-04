from pydantic import BaseModel, Field, validator


class RustBannedResponse(BaseModel):
    steamid: int = Field(..., alias='steamid64')
    twitter_url: str | None = Field(None, alias='url')
    days_ago: int | None = None
    is_banned: bool = Field(..., alias='eac_ban_count')

    @validator('is_banned', pre=True)
    def validate_eac_ban_count(cls, value: int) -> int:
        if int(value) > 1:
            return 1
        return int(value)

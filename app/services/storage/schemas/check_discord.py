from pydantic import BaseModel


class CheckDiscordBase(BaseModel):
    check_id: int
    discord_id: int


class CheckDiscordCreate(CheckDiscordBase):
    pass


class CheckDiscordUpdate(CheckDiscordBase):
    check_id: int | None = None
    discord_id: int | None = None


class CheckDiscordInDBBase(CheckDiscordBase):
    id: int

    class Config:
        orm_mode = True


class CheckDiscord(CheckDiscordInDBBase):
    pass


class CheckDiscordInDB(CheckDiscordInDBBase):
    pass

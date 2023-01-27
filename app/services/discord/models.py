from pydantic import BaseModel


class DiscordTag(BaseModel):
    username: str
    discriminator: int


class DiscordUser(BaseModel):
    id: str
    username: str
    discriminator: str


class DiscordRelationship(BaseModel):
    id: int
    type: str
    user: DiscordUser

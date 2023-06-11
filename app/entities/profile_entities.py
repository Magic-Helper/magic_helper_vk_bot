from pydantic import BaseModel


class ModeratorProfie(BaseModel):
    id: int
    name: str
    steamid: str
    vk_id: int
    is_superuser: bool

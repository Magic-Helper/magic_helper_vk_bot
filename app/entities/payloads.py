from pydantic import BaseModel


class GiveCheckerAccessPayload(BaseModel):
    give_checker_steamid: int

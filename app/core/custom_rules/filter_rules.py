from pydantic import BaseModel
from vkbottle.bot import rules


class TextInMessage(rules.ABCRule[rules.BaseMessageMin]):
    def __init__(self, text: str | list[str]) -> None:
        if isinstance(text, str):
            text = [text]

        self.text = text

    async def check(self, event: rules.BaseMessageMin) -> bool:
        for text in self.text:
            if text not in event.text:
                return False
        return True


class FromUserIdRule(rules.ABCRule[rules.BaseMessageMin]):
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def check(self, event: rules.BaseMessageMin) -> bool:
        return event.from_id == self.user_id


class PydanticPayloadRule(rules.ABCRule[rules.BaseMessageMin]):
    def __init__(self, payload_model: type[BaseModel]):
        self.payload_model = payload_model

    async def check(self, event: rules.BaseMessageMin) -> bool | dict[str, BaseModel]:
        payload = event.get_payload_json()
        if not payload.keys() == self.payload_model.__fields__.keys():
            return False
        return {'payload': self.payload_model(**payload)}

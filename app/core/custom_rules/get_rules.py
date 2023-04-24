from vkbottle import CtxStorage
from vkbottle.bot import rules

from app.services.api.check_api import CheckAPI
from app.tools import OnCheckStorage


class GetCheckAPI(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, event: rules.BaseMessageMin) -> CheckAPI:
        return {'check_api': CtxStorage().get('check_api')}


class GetCheckCollector(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, event: rules.BaseMessageMin) -> OnCheckStorage:
        return {'check_collector': CtxStorage().get('check_collector')}

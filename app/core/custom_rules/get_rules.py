from vkbottle import CtxStorage
from vkbottle.bot import rules

from app.services.api.check_api import CheckAPI
from app.tools import NicknamesToSteamidStorage, OnCheckStorage


#     ctx.set('on_check_storage', OnCheckStorage())
# ctx.set('nicknmaes_to_steamid_storage', NicknamesToSteamidStorage())
class GetCheckAPI(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, event: rules.BaseMessageMin) -> CheckAPI:
        return {'check_api': CtxStorage().get('check_api')}


class GetOnCheckStorage(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, event: rules.BaseMessageMin) -> OnCheckStorage:
        return {'on_check_storage': CtxStorage().get('on_check_storage')}


class GetNicknamesToSteamidStorage(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, event: rules.BaseMessageMin) -> NicknamesToSteamidStorage:
        return {'nicknames_to_steamid_storage': CtxStorage().get('nicknames_to_steamid_storage')}

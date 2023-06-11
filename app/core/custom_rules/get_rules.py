from vkbottle import API, CtxStorage
from vkbottle.bot import rules

from app.services.api import RCCAPI, CheckAPI, MagicRustAPI, ProfileAPI, ReportAPI
from app.tools import OnCheckStorage


class GetCheckAPI(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, event: rules.BaseMessageMin) -> CheckAPI:
        return {'check_api': CtxStorage().get('check_api')}


class GetCheckCollector(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, event: rules.BaseMessageMin) -> OnCheckStorage:
        return {'check_collector': CtxStorage().get('check_collector')}


class GetRCCAPI(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, event: rules.BaseMessageMin) -> RCCAPI:
        return {'rcc_api': CtxStorage().get('rcc_api')}


class GetMRAPI(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, event: rules.BaseMessageMin) -> MagicRustAPI:
        return {'mr_api': CtxStorage().get('mr_api')}


class GetReportAPI(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, event: rules.BaseMessageMin) -> ReportAPI:
        return {'report_api': CtxStorage().get('report_api')}


class GetRecordVKAPI(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, event: rules.BaseMessageMin) -> API:
        return {'record_vk_api': CtxStorage().get('record_vk_api')}


class GetProfileAPI(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, event: rules.BaseMessageMin) -> ProfileAPI:
        return {'profile_api': CtxStorage().get('profile_api')}

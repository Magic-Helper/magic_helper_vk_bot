from vkbottle import API
from vkbottle.bot import rules

from app.core import settings
from app.services.discord.discord_api import DiscordAPI
from app.services.discord.discord_client import DiscordClient
from app.services.magic_rust.MR_api import MagicRustAPI
from app.services.RCC.RCC_api import RustCheatCheckAPI
from app.services.storage.check_controller import (
    ChecksStorageController,
    OnCheckController,
)
from app.services.storage.check_discord_controller import CheckDiscordController
from app.services.storage.memory_storage import RCCDataMemoryStorage
from app.services.storage.report_controller import ReportController


class GetVKAPIRule(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, *args, **kwargs) -> dict:
        return {'vk_api': API(settings.VK_TOKEN)}


class GetMagicRustAPIRule(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, *args, **kwargs) -> dict:
        return {'magic_rust_api': MagicRustAPI()}


class GetRustCheatCheckAPIRule(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, *args, **kwargs) -> dict:
        return {'rcc_api': RustCheatCheckAPI()}


class GetChecksStorageControllerRule(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, *args, **kwargs) -> dict:
        return {'checks_storage': ChecksStorageController()}


class GetOnCheckControllerRule(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, *args, **kwargs) -> dict:
        return {
            'on_check_storage': OnCheckController(),
        }


class GetRCCDataMemoryStorageRule(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, *args, **kwargs) -> dict:
        return {'rcc_data_storage': RCCDataMemoryStorage()}


class GetDiscordAPIRule(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, *args, **kwargs) -> dict:
        return {'discord_api': DiscordAPI()}


class GetDiscordClientRule(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, *args, **kwargs) -> dict:
        return {'discord_client': DiscordClient()}


class GetCheckDiscordControllerRule(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, *args, **kwargs) -> dict:
        return {'check_discord_controller': CheckDiscordController()}


class GetReportControllerRule(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, *args, **kwargs) -> dict:
        return {'report_controller': ReportController()}

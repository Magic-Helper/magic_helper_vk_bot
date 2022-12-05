import re
from typing import TYPE_CHECKING, Optional, Union

from vkbottle import API
from vkbottle.bot import rules

from app.core import settings
from app.helpers.filtres import PlayerFilter
from app.services.magic_rust.MR_api import MagicRustAPI
from app.services.RCC.RCC_api import RustCheatCheckAPI
from app.services.storage.controller import OnCheckController


class OnCheckControllerRule(rules.ABCRule):
    async def check(self, *args, **kwargs) -> dict:
        return {
            'on_check_storage': OnCheckController(),
        }


class TextInMessage(rules.ABCRule[rules.BaseMessageMin]):
    def __init__(self, text: Union[str, list[str]]) -> None:
        if isinstance(text, str):
            text = [text]

        self.text = text

    async def check(self, event: rules.BaseMessageMin) -> bool:
        for text in self.text:
            if text not in event.text:
                return False
        return True


class SearchRegexRule(rules.ABCRule[rules.BaseMessageMin]):
    def __init__(self, regexp: Union[str, list[str], re.Pattern, list[re.Pattern]]):
        if isinstance(regexp, re.Pattern):
            regexp = [regexp]
        elif isinstance(regexp, str):
            regexp = [re.compile(regexp)]
        elif isinstance(regexp, list):
            regexp = [re.compile(exp) for exp in regexp]

        self.regexp = regexp

    async def check(self, event: rules.BaseMessageMin) -> Union[dict, bool]:
        for regexp in self.regexp:
            match = re.search(regexp, event.text)
            if match:
                return {'match': match.groups()}
        return False


class FromUserIdRule(rules.ABCRule[rules.BaseMessageMin]):
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def check(self, event: rules.BaseMessageMin) -> bool:
        return event.from_id == self.user_id


class MyCommandRule(rules.ABCRule[rules.BaseMessageMin]):
    """Represents a edited message rule with a custom check function.

    This rule is checks if args >= args_count
    """

    def __init__(
        self,
        command_text: Union[str, tuple[str, int]],
        prefixes: Optional[list[str]] = None,
        args_count: int = 0,
        sep: str = ' ',
    ):
        self.prefixes = prefixes or rules.DEFAULT_PREFIXES
        if isinstance(command_text, str):
            self.command_text = command_text
            self.args_count = args_count
        else:
            self.command_text, self.args_count = command_text
        self.sep = sep

    async def check(self, event: rules.BaseMessageMin) -> Union[dict, bool]:
        for prefix in self.prefixes:
            text_length = len(prefix + self.command_text)
            text_length_with_sep = text_length + len(self.sep)
            if event.text.startswith(prefix + self.command_text):
                if not self.args_count and len(event.text) == text_length:
                    return True
                if self.args_count and self.sep in event.text:
                    args = event.text[text_length_with_sep:].split(
                        self.sep, maxsplit=self.args_count
                    )
                    return {'args': args} if len(args) >= self.args_count and all(args) else False
        return False


class CommandListRule(rules.ABCRule[rules.BaseMessageMin]):
    """Rule for find a list of command in messsage"""

    def __init__(
        self,
        command_text: list[str],
        prefixes: Optional[list[str]] = None,
        args_count: int = 0,
        sep: str = ' ',
    ):
        self.command_text = command_text
        self.args_count = args_count
        self.prefixes = prefixes or rules.DEFAULT_PREFIXES
        self.sep = sep

    async def check(self, event: rules.BaseMessageMin) -> Union[dict, bool]:
        for prefix in self.prefixes:
            text_length = len(prefix + self.command_text)
            text_length_with_sep = text_length + len(self.sep)
            for command in self.command_text:
                if event.text.startswith(prefix + command):
                    if not self.args_count and len(event.text) == text_length:
                        return True
                    if self.args_count and self.sep in event.text:
                        args = event.text[text_length_with_sep:].split(
                            self.sep, maxsplit=self.args_count
                        )
                        return (
                            {'args': args} if len(args) == self.args_count and all(args) else False
                        )
        return False


class GetVKAPIRule(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, *args, **kwargs) -> dict:
        return {'vk_api': API(settings.VK_TOKEN)}


class GetMagicRustAPIRule(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, *args, **kwargs) -> dict:
        return {'magic_rust_api': MagicRustAPI()}


class GetRustCheatCheckAPIRule(rules.ABCRule[rules.BaseMessageMin]):
    async def check(self, *args, **kwargs) -> dict:
        return {'rcc_api': RustCheatCheckAPI()}


class GetPlayerFilterRule(rules.ABCRule[rules.BaseMessageMin]):
    def __init__(self, by_kd: float | None, by_check_on_magic: None | bool = False) -> None:
        """"""

    async def check(self, *args, **kwargs) -> dict:
        return {'player_filter': settings.PLAYER_FILTER}

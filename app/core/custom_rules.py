import re
from typing import Union, Optional

from vkbottle.bot import rules

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
    def __init__(
        self,
        command_text: Union[str, tuple[str, int]],
        prefixes: Optional[list[str]] = None,
        args_count: int = 0,
        sep: str = " ",
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
                elif self.args_count and self.sep in event.text:
                    args = event.text[text_length_with_sep:].split(self.sep, maxsplit=self.args_count)
                    return {"args": args} if len(args) == self.args_count and all(args) else False
        return False
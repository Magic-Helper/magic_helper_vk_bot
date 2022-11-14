import re
from typing import Union

from vkbottle.bot import rules


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

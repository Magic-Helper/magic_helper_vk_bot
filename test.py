import asyncio
import re

from vkbottle.bot import rules

from app.custom_rules import SearchRegexRule


class TestEvent:
    def __init__(self, text: str):
        self.text = text


regexp = r'вызван на проверку'
# regexp = re.compile(test_regexp, re.MULTILINE)


regex_rule = rules.RegexRule(regexp)
my_rule = SearchRegexRule(regexp)


start_check = '@id163811405 твоя команда выполнена.\nОтвет: Lil Quest ? вызван на проверку. Напишите /cc2 8 76561198233873852 для отмены проверки.\nИгрок бездействует 5 секунд.'
event = TestEvent(start_check)


# print(regexp.search(start_check))

result = asyncio.run(regex_rule.check(event))
result2 = asyncio.run(my_rule.check(event))

print(result)
print(result2)

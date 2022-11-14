DAY_WORK_MONTH_END = 9
TIMEZONE = 'Europe/Moscow'
STRING_DATE_FORMAT = 'DD.MM.YYYY'

VK_REPORT_GROUP_ID = -179043503
VK_RECORDS_GROUP_ID = -166700992


class VK_FOR_CMD:  # MAGICRUST Отчеты
    id_: int = 166700992


class VK_FOR_MESSAGE:  # MAGIC HELPER
    id_: int = 215360486


GROUP_IDS = [VK_FOR_CMD.id_, VK_FOR_MESSAGE.id_]


class REGEX_PATTERNS:
    VK_ID = r'\[id(\d+)\|'  # -> [id`163811405`|@mahryct]
    STRING_IS_DATE = r'\d{,2}.\d{2}.\d{4}-\d{,2}.\d{2}.\d{4}'  # -> `9.04.2022-8.05.2022`
    STEAMID = r'/cc2 \d{,2} (\d+) для'
    NICKNAME = r'Ответ:\s(.+)\s[бвз][оыа][лзб]'
    SERVER_NUMBER = r'/cc2\s(\d+)\s'

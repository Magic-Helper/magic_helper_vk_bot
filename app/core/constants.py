DAY_WORK_MONTH_END = 8
TIMEZONE = 'Europe/Moscow'
STRING_DATE_FORMAT = 'DD.MM.YYYY'

VK_REPORT_GROUP_ID = -179043503
VK_RECORDS_GROUP_ID = -166700992

# Агрументы по дефолту если не указаны
DEFAULT_TIME_PASSED = '30d'
DEFAULT_BIG_KD = 10.0

OWNER_VK_ID = 163811405


class VK_FOR_CMD:  # MAGICRUST Отчеты
    id_: int = 166700992


class VK_FOR_MESSAGE:  # MAGIC HELPER
    id_: int = 215360486
    magic_records_peer_id: int = 2000000002
    available_users: list[int] = [VK_RECORDS_GROUP_ID, VK_REPORT_GROUP_ID]


GROUP_IDS = [VK_FOR_CMD.id_, VK_FOR_MESSAGE.id_]


# Паттерны для парсинга информация из сообщений от бота магик отчетов
class REGEX_PATTERNS:
    VK_ID = r'\[id(\d+)\|'  # -> [id`163811405`|@mahryct]
    STRING_IS_DATE = r'\d{,2}.\d{2}.\d{4}-\d{,2}.\d{2}.\d{4}'  # -> `9.04.2022-8.05.2022`
    STEAMID = r'/cc2 \d{,2} (\d+) для'  # -> /cc2 1 `76561198324984465` для
    NICKNAME = r'Ответ:\s(.+)\s[бвз][оыа][лзб]'  # -> Ответ: `AntiSocial 妻マwatch me dieマ` больше не проверяется/вызван на проверку/забанен с причиной # noqa
    SERVER_NUMBER = r'/cc2\s(\d+)\s'  # -> /cc2 `1` 76561198324984465 для
    NICKNAME_IN_REPORT = r'Игрок (.+) предоставил '


class RUST_REPORT_REGEX:
    SERVER_NUMBER = r'🤡 (.*)-й'
    AUTHOR_NICKNAME = r'от игрока (.*).'
    REPORT_STEAMID = r'\.com/profiles/(.*)\)'


class MAGIC_REPORT_REGEX:
    SERVER_NUMBER = r'(\d+)-й'
    AUTHOR_NICKNAME = r'от игрока (.*) на'
    REPORT_STEAMID = r'profiles/(\d+)'


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'


AVAILABLE_BAN_REASONS: list[str] = [
    'чит',
    'cheat',
    'macro',
    'макро',
    'eac',
    'еак',
    'm-a',
    'm/a',
    'м/а',
    'multiacc',
    'мультиакк',
    'покинул',
    'отказ',
    'disconnect',
    'вышел',
    'выход',
    'leave',
    'игнор',
    'ignore',
    'результатам',
    'просвет',
    'неверные',
    'чистка',
]

NOT_AVAILABLE_BAN_REASONS: list[str] = [
    'игра с читером',
    'game with cheater',
    'you had eac ban on your account',
    'тим чит',
]


RUST_SERVERS_NAME: list[str] = [
    'MAGIC',
    'MR',
    'GRAND',
    'TRAVELER',
    'ULTIMATE',
    'ROOM',
    'BEARZ',
    'BRO',
    'ORION',
    'FUNRUST',
    'BOLOTO',
    'MAGMA',
    'TOFFS',
]

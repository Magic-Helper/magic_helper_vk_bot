from enum import Enum

DAY_WORK_MONTH_END = 8
TIMEZONE = 'Europe/Moscow'
STRING_DATE_FORMAT = 'DD.MM.YYYY'
EMPTY_SYM = '⠀'

# Bans
DEFAULT_DAYS_PASSED_AFTER_BAN = 60

# Stats
DAYS_WHILE_PLAYER_NEW = 60
MIN_STATS_FOR_NEW_PLAYER = 1.0
MIN_STATS_FOR_PLAYER = 10.0

# Reports
HOW_DAYS_DONT_SHOW_PLAYER_IN_REPORTS = 30  # После проверки
DEAFULT_MIN_REPORTS = 3  # Для отображения

# Checks
REMOVE_GIVE_ACCCESS_PAYLOAD_DELAY = 60 * 30

VK_REPORT_GROUP_ID = -179043503
VK_RECORDS_GROUP_ID = -166700992


class VK_MAGIC_RECORDS:  # MAGICRUST Отчеты
    id_: int = 166700992
    chat_peer_id = 2000000005


class VK_MAGIC_HELPER:  # MAGIC HELPER
    id_: int = 215360486
    chat_peer_id: int = 2000000002
    available_users: list[int] = [VK_RECORDS_GROUP_ID, VK_REPORT_GROUP_ID]


GROUP_IDS = [VK_MAGIC_RECORDS.id_, VK_MAGIC_HELPER.id_]


class BotTypes(Enum):
    MAGIC_RECORDS_BOT = 'magic_records_bot'
    MAGIC_HELPER_BOT = 'magic_helper_bot'


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

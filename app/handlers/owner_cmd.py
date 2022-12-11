from typing import TYPE_CHECKING

from loguru import logger
from pympler import asizeof
from vkbottle.bot import BotLabeler, rules

from app.core import constants
from app.helpers.custom_rules import GetRCCDataMemoryStorageRule
from app.services.storage.memory_storage import OnCheckMemoryStorage

if TYPE_CHECKING:
    from vkbottle.bot import Message

    from app.services.storage.memory_storage import RCCDataMemoryStorage

labeler = BotLabeler()
labeler.auto_rules = [rules.FromPeerRule(constants.OWNER_VK_ID)]


@labeler.message(rules.CommandRule('rcc_data_info', prefixes=['/', '.']), GetRCCDataMemoryStorageRule())
async def get_rcc_memory_storage_info(message: 'Message', rcc_data_storage: 'RCCDataMemoryStorage') -> None:
    """Handle /rcc_data_info command and send info about rcc_data_storage to chat"""
    size = f'Размер рцц хранилища: {asizeof.asizeof(rcc_data_storage) / 1024 / 1024:.2f} мб\n'
    count_players = f'Количество игроков в хранилище: {len(rcc_data_storage._players)}\n'
    count_steamids_with_data = f'Количество steamids c данными: {len((rcc_data_storage._players.keys))}\n'
    count_steamids_no_data = f'Количество steamids без данных: {len(rcc_data_storage._cached_steamids)}\n'
    msg = size + count_players + count_steamids_with_data + count_steamids_no_data
    logger.debug(msg)
    await message.answer(msg)


@labeler.message(rules.CommandRule('rcc_data_steamids', prefixes=['/', '.']), GetRCCDataMemoryStorageRule())
async def get_rcc_data_steamids(message: 'Message', rcc_data_storage: 'RCCDataMemoryStorage') -> None:
    """Handle /rcc_data_steamids command and send all steamids to chat"""
    steamids = rcc_data_storage.get_players_data_exists()
    logger.debug(steamids)
    await message.answer(f'Стиайдишники для которых есть инфа{steamids}')


@labeler.message(rules.CommandRule('rcc_data_clear', prefixes=['/', '.']), GetRCCDataMemoryStorageRule())
async def clear_rcc_data(message: 'Message', rcc_data_storage: 'RCCDataMemoryStorage') -> None:
    """Handle /rcc_data_clear command and clear rcc data storage"""
    rcc_data_storage.clear_data()
    logger.info('RCC data storage cleared')
    await message.answer('РЦЦ Хранлище очищено')


@labeler.message(rules.CommandRule('on_checks_plaeyrs'))
async def get_on_checks_players(message: 'Message') -> None:
    """Handle /on_checks_players command and send all players on checks to chat"""
    on_check_storage = OnCheckMemoryStorage()
    nicknames = on_check_storage._nicknames_to_steamids
    players = on_check_storage._on_check
    logger.debug(nicknames)
    logger.debug(players)
    msg = f'Никнеймы: {nicknames}\nИгроки: {players}'
    await message.answer(msg)

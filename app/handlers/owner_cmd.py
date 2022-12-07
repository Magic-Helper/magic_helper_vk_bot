from typing import TYPE_CHECKING

from vkbottle.bot import BotLabeler, rules
from pympler import asizeof
from loguru import logger

from app.helpers.custom_rules import GetRCCDataMemoryStorageRule

if TYPE_CHECKING:
    from vkbottle.bot import Message

    from app.services.storage.memory_storage import RCCDataMemoryStorage

labeler = BotLabeler()


@labeler.message(
    rules.CommandRule('rcc_data_info', prefixes=['/', '.']), GetRCCDataMemoryStorageRule()
)
async def get_rcc_memory_storage_info(
    message: 'Message', rcc_data_storage: 'RCCDataMemoryStorage'
) -> None:
    """Handle /rcc_data_info command and send info about rcc_data_storage to chat"""
    # Get size of rcc data storage in mb
    msg = f'Размер рцц хранилища: {asizeof.asizeof(rcc_data_storage) / 1024 / 1024} мб'
    logger.debug(msg)
    # await message.answer(msg)


@labeler.message(
    rules.CommandRule('rcc_data_all', prefixes=['/', '.']), GetRCCDataMemoryStorageRule()
)
async def get_all_rcc_memory_storage(
    message: 'Message', rcc_data_storage: 'RCCDataMemoryStorage'
) -> None:
    """Handle /rcc_data_all command and send all rcc data to chat"""
    # Get all rcc data from storage
    exists_players_steamid = rcc_data_storage.get_players_data_exists()
    msg = rcc_data_storage.get_players(exists_players_steamid)
    logger.debug(msg)
    # await message.answer(msg)

from vkbottle.bot import rules

from app.services.storage import MemoryStorage
from app.services.storage.controller import ChecksStorage


class StorageControllersRule(rules.ABCRule):
    async def check(self, *args, **kwargs) -> dict:
        return {
            'checks_storage': ChecksStorage(),
            'memory_storage': MemoryStorage(),
        }

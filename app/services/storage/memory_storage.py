from typing import TYPE_CHECKING, Any, Generic, TypeVar, Union

from app.core.utils import singleton

if TYPE_CHECKING:
    from app.core.typedefs import Nickname, StageData, Steamid


StorageKey = TypeVar('StorageKey', bound=Any)
StorageValue = TypeVar('StorageValue', bound=Any)


class MemoryStorage(Generic[StorageKey, StorageValue]):
    def __init__(self) -> None:
        self.storage: dict[StorageKey, StorageValue] = {}

    def update(self, key: StorageKey, value: StorageValue) -> None:
        self.storage[key] = value

    def get(self, key: StorageKey) -> StorageValue:
        return self.storage.get(key)

    def delete(self, key: StorageKey) -> None:
        del self.storage[key]

    def pop(self, key: StorageKey) -> StorageValue:
        return self.storage.pop(key)


@singleton
class StageDataMemoryStorage(MemoryStorage['Steamid', 'StageData']):
    pass


@singleton
class NicknamesMemoryStorage(MemoryStorage['Nickname', 'Steamid']):
    pass

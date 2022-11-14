from typing import TYPE_CHECKING, Union, TypeVar, Any, Generic
from abc import ABC

from app.core.utils import singleton

if TYPE_CHECKING:
    from app.core.typedefs import StageData, Steamid, Nickname


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

    def pop(self, key: StorageKey) -> dict[StorageKey, StorageValue]:
        return self.storage.pop(key)

@singleton
class CheckMemoryStorage(MemoryStorage[Union['Steamid', 'Nickname'], 'StageData']):
    def update(self, steamid: 'Steamid', nickname: 'Nickname', value: 'StageData') -> None:
        """Update storage with steamid and nickname keys.
        
        Args:
            steamid (Steamid): Steamid of player.
            nickname (Nickname): Nickname of player.
            value (StageData): Stage data.
        """
        self.storage[steamid] = value
        self.storage[nickname] = value
    
    def delete(self, nickname: 'Nickname') -> None:
        """Delete storage by nickname.
        
        Args:
            nickname (Nickname): Nickname of player.
        """
        steamid = self.get(nickname).steamid
        del self.storage[steamid]
        del self.storage[nickname]
    
    def pop(self, nickname: 'Nickname') -> 'StageData':
        """Pop storage by nickname.
        
        Args:
            nickname (Nickname): Nickname of player.
        
        Returns:
            StageData: Stage data.
        """
        data = self.storage.pop(nickname)
        del self.storage[data.steamid]
        return data
    
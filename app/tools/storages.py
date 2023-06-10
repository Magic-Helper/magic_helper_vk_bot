from typing import Generic, TypeAlias, TypeVar

from vkbottle.tools import ABCStorage

from app.entities import OnCheck

KeyType = TypeVar('KeyType')
ValueType = TypeVar('ValueType')

Steamid: TypeAlias = str


class BaseStorage(ABCStorage, Generic[KeyType, ValueType]):
    def __init__(self):
        self._storage = {}

    def get(self, key: KeyType) -> ValueType | None:
        return self._storage.get(key)

    def set(self, key: KeyType, value: ValueType) -> None:
        self._storage[key] = value

    def delete(self, key: KeyType) -> ValueType:
        return self._storage.pop(key)

    def contains(self, key: KeyType) -> bool:
        return key in self._storage

    def clear(self) -> None:
        self._storage.clear()


class OnCheckStorage(BaseStorage[Steamid, OnCheck]):
    pass


class NicknamesToSteamidStorage(BaseStorage[str, Steamid]):
    pass

from typing import Generic, TypeVar

from vkbottle.tools import ABCStorage

from app.entities import OnCheck

KeyType = TypeVar('KeyType')
ValueType = TypeVar('ValueType')


class BaseStorage(ABCStorage, Generic[KeyType, ValueType]):
    def __init__(self):
        self._storage = {}

    def get(self, key: KeyType) -> ValueType | None:
        return self._storage.get(key)

    def set(self, key: KeyType, value: ValueType) -> None:
        self._storage[key] = value

    def delete(self, key: KeyType) -> None:
        self._storage.pop(key)

    def contains(self, key: KeyType) -> bool:
        return key in self._storage


class OnCheckStorage(BaseStorage[int, OnCheck]):
    pass


class NicknamesToSteamidStorage(BaseStorage[str, int]):
    pass

from typing import Generic, TypeVar

from vkbottle.tools import ABCStorage

from app.entities import OnCheck

KeyType = TypeVar('KeyType')
ValueType = TypeVar('ValueType')


class BaseStorage(ABCStorage, Generic[KeyType, ValueType]):
    def __init__(self):
        self.__storage = {}

    def get(self, key: KeyType) -> ValueType | None:
        return self.__storage.get(key)

    def set(self, key: KeyType, value: ValueType) -> None:
        self.__storage[key] = value

    def delete(self, key: KeyType) -> None:
        self.__storage.pop(key)

    def contains(self, key: KeyType) -> bool:
        return key in self.__storage


class OnCheckStorage(BaseStorage[int, OnCheck]):
    pass


class NicknamesToSteamidStorage(BaseStorage[str, int]):
    pass


on_check_storage = OnCheckStorage()
nickname_to_steamid_storage = NicknamesToSteamidStorage()

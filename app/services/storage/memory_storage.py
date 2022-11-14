from typing import TYPE_CHECKING

from app.core.utils import singleton

if TYPE_CHECKING:
    from app.core.typedefs import StageData


@singleton
class MemoryStorage:
    def __init__(self) -> None:
        self.storage: dict[str, 'StageData'] = {}

    def update(self, key: str, value: 'StageData') -> None:
        self.storage[key] = value

    def get(self, key: str) -> 'StageData':
        return self.storage[key]

    def delete(self, key: str) -> None:
        del self.storage[key]

    def pop(self, key: str) -> 'StageData':
        return self.storage.pop(key)

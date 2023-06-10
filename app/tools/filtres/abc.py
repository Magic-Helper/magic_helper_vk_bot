from abc import ABC, abstractmethod
from typing import Any


class ABCFilter(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def execute(self, data: Any) -> Any:
        ...

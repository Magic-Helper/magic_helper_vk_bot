from abc import ABC, abstractmethod


class ABCUserView(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def render(self) -> str:
        ...

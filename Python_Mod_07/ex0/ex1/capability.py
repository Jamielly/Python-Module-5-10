from abc import ABC, abstractmethod
from typing import Optional


class HealCapability(ABC):

    @abstractmethod
    def heal(self, target: Optional[str] = None) -> str:
        pass


class TransformCapability(ABC):

    def __init__(self) -> None:
        self._transformed: bool = False

    @abstractmethod
    def transform(self) -> str:
        pass

    @abstractmethod
    def revert(self) -> str:
        pass

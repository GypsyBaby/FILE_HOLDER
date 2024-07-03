from abc import ABC, abstractmethod
from _hashlib import HASH


class IHashComponent(ABC):

    @property
    @abstractmethod
    def hasher(self): ...

    @abstractmethod
    def hash(self, file_data: bytes) -> str: ...

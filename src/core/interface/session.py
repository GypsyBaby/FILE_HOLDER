from abc import ABC, abstractmethod
from typing import ContextManager
from sqlalchemy.orm import sessionmaker, Session


class ISessionSyncFactory(ABC):
    @property
    @abstractmethod
    def maker(self) -> sessionmaker:
        pass


class ISessionSyncWrapper(ABC):
    @property
    @abstractmethod
    def factory(self) -> ISessionSyncFactory:
        pass

    @abstractmethod
    def t(self) -> ContextManager[Session]:
        pass

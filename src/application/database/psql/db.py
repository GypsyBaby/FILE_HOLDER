import json
from contextlib import contextmanager

from sqlalchemy import Engine, MetaData
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from typing import ContextManager
from sqlalchemy import create_engine as sa_create_engine

from src.core.interface.session import (
    ISessionSyncWrapper,
    ISessionSyncFactory,
)


def create_sync_engine(url: str):
    return sa_create_engine(
        url,
        pool_pre_ping=False,
        echo=False,
        json_serializer=lambda x: json.dumps(x, ensure_ascii=False),
    )


class SessionSyncFactory(ISessionSyncFactory):
    def __init__(self, engine: Engine) -> None:
        self._maker = sessionmaker(
            engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    @property
    def maker(self) -> sessionmaker[Session]:
        return self._maker


class SessionSyncWrapper(ISessionSyncWrapper):
    def __init__(self, factory: ISessionSyncFactory) -> None:
        self._factory = factory

    @property
    def factory(self) -> ISessionSyncFactory:
        return self._factory

    def t(self) -> ContextManager[Session]:
        @contextmanager  # type: ignore
        def wrapped() -> ContextManager[Session]:  # type: ignore
            with self.factory.maker() as session:
                try:
                    yield session  # type: ignore
                except Exception as e:
                    session.rollback()
                    raise e
                finally:
                    session.close()

        return wrapped()


convention = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "ix": "ix_%(table_name)s_%(column_0_name)s",
}

meta = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    """Base cls for models"""

    metadata = meta

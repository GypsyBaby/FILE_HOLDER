import re
from typing import Optional, Tuple, Type
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import and_, delete, func, literal_column, select

from src.core.interface.session import ISessionSyncWrapper

from src.core.interface.repo.psql import IPSQLSyncRepo
from src.core.exceptions.db import RelationError, UniqueError, FormatError
from src.core.dto.file import FileCreateDTO, FileDTO, FileFilter
from src.core.dto.user import UserFilter, UserDTO

from src.data.models import File as FileModel, User as UserModel


PG_REGEX_DETAIL = r"DETAIL:  (.*?) \["


def parse_db_error(e: Exception) -> Tuple[Optional[Type[Exception]], Optional[str]]:
    if not hasattr(e, "orig"):
        return None, None
    if not hasattr(e.orig, "pgcode"):  # type: ignore
        return None, None
    undescribed_error = "Undescribed error"
    message_of_e = str(e).replace("\n", " ")
    pgcode = e.orig.pgcode  # type: ignore
    if pgcode == "23503":
        exc_cls = RelationError
        exc_msg = "Related entity not found error"
    elif pgcode == "23505":
        exc_cls = UniqueError
        exc_msg = "Unique validation error"
    elif pgcode == "42P10":
        exc_cls = FormatError
        exc_msg = "Conflict field error"
    elif pgcode == "22000":
        exc_cls = FormatError
        exc_msg = "Invalid args"
    else:
        return None, None

    match = re.search(PG_REGEX_DETAIL, message_of_e)
    error_format_trace = match.group(1).replace('"', "") if match else undescribed_error
    return (exc_cls, f"{exc_msg}: {error_format_trace}")


class PSQLSyncRepo(IPSQLSyncRepo):
    def __init__(self, session_wrapper: ISessionSyncWrapper) -> None:
        # self._session: Optional[Session] = None
        with session_wrapper.t() as session:
            self._session = session

    @property
    def session(self) -> Session:
        if self._session is None:
            raise NotImplementedError("Session was not setup")
        return self._session

    def commit(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            t, txt = parse_db_error(e)
            if t is None:
                raise
            raise t(txt) from e

    def _flush(self):
        try:
            self.session.flush()
        except Exception as e:
            self.session.rollback()
            t, txt = parse_db_error(e)
            if t is None:
                raise
            raise t(txt) from e

    def get_file(self, fltr: FileFilter) -> Optional[FileDTO]:
        stmt = select(FileModel)
        if isinstance(fltr.name, str):
            stmt = stmt.where(FileModel.name == fltr.name)
        if isinstance(fltr.owner_id, int):
            stmt = stmt.where(FileModel.owner_id == fltr.owner_id)
        model = self.session.scalar(stmt)
        if model is None:
            return None
        return FileDTO(
            id=model.id, name=model.name, extension=model.extension, owner_id=model.owner_id
        )

    def create_file(self, file_create_dto: FileCreateDTO) -> FileDTO:
        model = FileModel(
            name=file_create_dto.name,
            extension=file_create_dto.extension,
            owner_id=file_create_dto.owner_id,
        )
        self.session.add(model)
        self._flush()
        return FileDTO(
            id=model.id, name=model.name, extension=model.extension, owner_id=model.owner_id
        )

    def get_user(self, fltr: UserFilter) -> Optional[UserDTO]:
        stmt = select(UserModel)
        if isinstance(fltr.id, int):
            stmt = stmt.where(UserModel.id == fltr.id)
        if isinstance(fltr.login, str):
            stmt = stmt.where(UserModel.login == fltr.login)
        model = self.session.scalar(stmt)
        if model is None:
            return None
        return UserDTO(id=model.id, login=model.login, password=model.password)

    def delete_file(self, id: int) -> None:
        stmt = delete(FileModel).where(FileModel.id == id)
        self.session.execute(stmt)
        self._flush()
        return

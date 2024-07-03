from abc import ABC, abstractmethod
from typing import Optional

from src.core.dto.file import FileCreateDTO, FileDTO, FileFilter
from src.core.dto.user import UserFilter, UserDTO

class IPSQLSyncRepo(ABC):

    @abstractmethod
    def commit() -> None:
        ...

    @abstractmethod
    def get_file(self, fltr: FileFilter) -> Optional[FileDTO]:
        ...

    @abstractmethod
    def create_file(self, file_create_dto: FileCreateDTO) -> FileDTO:
        ...

    @abstractmethod
    def delete_file(self, id: int) -> None:
        ...

    def get_user(self, fltr: UserFilter) -> Optional[UserDTO]:
        ...
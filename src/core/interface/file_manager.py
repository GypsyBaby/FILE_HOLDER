from abc import ABC, abstractmethod
from werkzeug.datastructures import FileStorage


class IFileManager(ABC):

    @abstractmethod
    def create_dir_if_not_exist(self, dir_name: str) -> None: ...

    @abstractmethod
    def save_on_disk(self, file: FileStorage, dir_name: str) -> None: ...

    @abstractmethod
    def delete_file_if_exist(self, file_name: str, dir: str) -> None: ...

    @abstractmethod
    def dir_exist(self, dir_name: str) -> bool: ...

    @abstractmethod
    def send_file_if_exist(self, file_name: str, dir: str) -> None: ...

    @abstractmethod
    def file_exist(self, file_name: str, dir: str) -> bool: ...

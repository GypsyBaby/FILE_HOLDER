import os
from typing import Optional
from pathlib import Path
from werkzeug.datastructures import FileStorage
from flask import Response, send_from_directory

from src.core.interface.file_manager import IFileManager
from src.core.exceptions.file_manager import FileManagerError


class FileManager(IFileManager):

    def __init__(self, root_dir: str) -> None:
        self._root_dir = root_dir

    def create_dir_if_not_exist(self, dir_name: str) -> None:
        dir_path = Path(self._root_dir, dir_name)
        if not self.dir_exist(dir_name=dir_name):
            try:
                os.makedirs(name=dir_path, exist_ok=True)
            except Exception as e:
                raise FileManagerError(
                    f"Error on create dir with path: `{dir_path}`"
                ) from e

    def save_on_disk(self, file: FileStorage, dir_name: str) -> None:
        file_name = str(file.filename)
        dir_path = os.path.join(self._root_dir, dir_name, file_name)
        try:
            file.stream.seek(0)
            file.save(dst=dir_path)
        except Exception as e:
            raise FileManagerError(
                f"Error on save file `{file.name}` on path `{dir_path}`"
            ) from e

    def dir_exist(self, dir_name: str) -> bool:
        dir_path = Path(self._root_dir, dir_name)
        try:
            dir_exist = os.path.isdir(dir_path)
        except Exception as e:
            raise FileManagerError(f"Problem with dir path `{dir_path}`") from e
        return dir_exist

    def delete_file_if_exist(self, file_name: str, dir: str) -> None:
        file_path = Path(self._root_dir, dir, file_name)
        file_exist = self._file_exist(file_path=file_path)
        if not file_exist:
            return
        try:
            os.remove(path=file_path)
        except Exception as e:
            raise FileManagerError(f"Error `{e}` while deleting file {file_path=}")
        return

    def send_file_if_exist(self, file_name: str, dir: str) -> Optional[Response]:
        file_path = Path(self._root_dir, dir, file_name)
        file_exist = self._file_exist(file_path=file_path)
        if not file_exist:
            return
        dir_path = Path(self._root_dir, dir)
        try:
            return send_from_directory(
                directory=dir_path, path=file_name, as_attachment=True
            )
        except Exception as e:
            raise FileManagerError(f"Error `{e}` on send file with path `{file_path}`")

    def file_exist(self, file_name: str, dir: str) -> bool:
        file_path = Path(self._root_dir, dir, file_name)
        return self._file_exist(file_path=file_path)

    def _file_exist(self, file_path: Path) -> bool:
        try:
            return os.path.isfile(path=file_path)
        except Exception as e:
            raise FileManagerError(f"Problem with file path `{file_path}`") from e

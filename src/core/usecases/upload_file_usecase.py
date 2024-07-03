from typing import Tuple

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from src.core.interface.hash import IHashComponent
from src.core.interface.file_manager import IFileManager
from src.core.interface.repo.psql import IPSQLSyncRepo
from src.core.dto.file import FileCreateDTO


class UploadUsecaseError(Exception): ...


class Usecase:

    def __init__(
        self,
        hash_component: IHashComponent,
        file_manager: IFileManager,
        repo: IPSQLSyncRepo,
    ) -> None:
        self.hash_component = hash_component
        self.file_manager = file_manager
        self.repo = repo

    def _get_two_first_letters(self, s: str) -> str:
        return s[:2]

    def _get_file_extension(self, file_name: str) -> str:
        try:
            return file_name.split(".")[-1]
        except Exception as e:
            raise Exception(
                f"Error `{e}` on get file extension by filename: `{file_name}`"
            )

    def _rename_file_as_hash(self, file: FileStorage, hash_name: str) -> None:
        file_name = file.filename
        if file_name is None:
            raise UploadUsecaseError("File name is None!!!")
        file_name = secure_filename(file_name)
        extension = self._get_file_extension(file_name)
        file_name = ".".join([hash_name, extension])
        try:
            file.filename = file_name
        except Exception as e:
            raise UploadUsecaseError(f"Error `{e}` on reaname file `{file.name}`")

    def _separate_name_and_extension(self, file_name: str) -> Tuple[str, str]:
        parts = file_name.split(".")
        if len(parts) != 2:
            raise UploadUsecaseError(f"If file name `{file_name}` can be only one '.'")
        name, extension = parts
        return name, extension

    def __call__(self, file: FileStorage, owner_id: int) -> str:
        try:
            file_bytes = file.read()
        except Exception as e:
            raise UploadUsecaseError(f"Error {e} on read bytes of file {file.name}")
        if file.filename is None:
            raise UploadUsecaseError("File name can not be None!")
        _, ext = self._separate_name_and_extension(file_name=file.filename)
        file_hash = self.hash_component.hash(file_data=file_bytes)
        dir_name = self._get_two_first_letters(file_hash)
        file_name = ".".join([file_hash, ext])
        file_exist = self.file_manager.file_exist(file_name=file_name, dir=dir_name)
        if file_exist:
            return file_hash
        try:
            self.file_manager.create_dir_if_not_exist(dir_name=dir_name)
        except Exception as e:
            raise UploadUsecaseError(f"Error `{e}` on process dir `{dir_name}`")
        self._rename_file_as_hash(file=file, hash_name=file_hash)
        try:
            self.file_manager.save_on_disk(file=file, dir_name=dir_name)
        except Exception as e:
            raise UploadUsecaseError(f"Error `{e}` on save file in dir `{dir_name}`")
        assert file.filename  # just for typings
        file_name, extension = self._separate_name_and_extension(
            file_name=file.filename
        )
        try:
            self.repo.create_file(
                file_create_dto=FileCreateDTO(
                    name=file_name, extension=extension, owner_id=owner_id
                )
            )
            self.repo.commit()
        except Exception as e:
            raise UploadUsecaseError(f"Error `{e}` while create file in DB")
        return file_hash

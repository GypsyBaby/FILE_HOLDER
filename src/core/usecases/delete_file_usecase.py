from src.core.interface.file_manager import IFileManager
from src.core.interface.repo.psql import IPSQLSyncRepo
from src.core.dto.file import FileFilter


class DeleteUsecaseError(Exception): ...


class Usecase:

    def __init__(
        self,
        file_manager: IFileManager,
        repo: IPSQLSyncRepo,
    ) -> None:
        self.file_manager = file_manager
        self.repo = repo

    def _get_two_first_letters(self, s: str) -> str:
        return s[:2]

    def _join_name_and_extension(self, n: str, e: str) -> str:
        return ".".join([n, e])

    def __call__(self, file_name: str, user_id: int) -> None:
        try:
            file_model = self.repo.get_file(fltr=FileFilter(name=file_name))
        except Exception as e:
            raise DeleteUsecaseError(f"Error `{e}` while getting file {file_name}")
        if file_model is None:
            return
        if file_model.owner_id != user_id:
            return
        dir_name = self._get_two_first_letters(file_name)
        try:
            dir_exist = self.file_manager.dir_exist(dir_name)
        except Exception as e:
            raise DeleteUsecaseError(f"Error `{e}` while call dir_exist() func")
        if not dir_exist:
            return
        file_name = self._join_name_and_extension(n=file_name, e=file_model.extension)
        try:
            self.file_manager.delete_file_if_exist(file_name=file_name, dir=dir_name)
        except Exception as e:
            raise DeleteUsecaseError(f"Error `{e}` while deleting file {file_name}")
        try:
            self.repo.delete_file(id=file_model.id)
            self.repo.commit()
        except Exception as e:
            raise DeleteUsecaseError(
                f"Error `{e}` while deleting file `{file_name}` from db"
            )
        return

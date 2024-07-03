import pytest
from settings import settings
from src.core.components.file_manager import FileManager


@pytest.fixture(scope="function")
def file_manager():
    return FileManager(root_dir=settings.UPLOAD_FOLDER)

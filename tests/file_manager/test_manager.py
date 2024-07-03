import pytest
from tests.file_manager.conftest import *

# pytest tests\file_manager\test_manager.py::test_create_dir -v -s
def test_create_dir(file_manager):
    fm = file_manager
    fm.create_dir_if_not_exist(dir_path="filestore/pipa/boba")

import pytest
from tests.hash_comp.conftest import *


# pytest tests\hash_comp\test_hash.py::test_hash_comp -v -s
@pytest.mark.parametrize("input, output", [
    (b"aboba", "150f15e73422e0a5ba5b59f997fc2350"),
    (b"some_file_bytes_bla_bla_bla_bla", "af22fc5a32b0d610bf5e2bae4413558c")
])
def test_hash_comp(hasher_md5, input, output):
    hash_result = hasher_md5.hash(file=input)
    assert hash_result == output

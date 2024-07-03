import pytest

from src.core.components.hash import HashComponent


@pytest.fixture(scope="function")
def hasher_md5():
    hc = HashComponent()
    hc.configure(hash_alg="md5")
    return hc

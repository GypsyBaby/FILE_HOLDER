import hashlib
from _hashlib import HASH

from src.core.interface.hash import IHashComponent
from src.core.exceptions.hash import HashComponentError, HashComponentConfigureError


class HashComponent(IHashComponent):

    def __init__(self, hash_alg: str) -> None:
        try:
            hasher = hashlib.new(hash_alg)
        except Exception as e:
            raise HashComponentConfigureError(
                f"Fail on configure HashComponent. Error: {e}"
            ) from e
        self._hasher = hasher

    @property
    def hasher(self) -> HASH:
        if self._hasher is None:
            raise HashComponentError("Hash component is not configured")
        return self._hasher

    def hash(self, file_data: bytes) -> str:
        try:
            self.hasher.update(file_data)
            result = self.hasher.hexdigest()
        except Exception as e:
            raise HashComponentError(f"Fail on get hash of file") from e
        return result

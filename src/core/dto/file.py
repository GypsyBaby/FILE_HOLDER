from typing import Optional
from dataclasses import dataclass


@dataclass
class FileDTO:
    id: int
    name: str
    extension: str
    owner_id: int


@dataclass
class FileCreateDTO:
    name: str
    extension: str
    owner_id: int


@dataclass
class FileFilter:
    name: Optional[str] = None
    owner_id: Optional[int] = None

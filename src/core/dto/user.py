from typing import Optional
from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int
    login: str
    password: str


@dataclass
class UserFilter:
    id: Optional[int] = None
    login: Optional[str] = None

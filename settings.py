import os
from pathlib import Path
from pydantic import BaseSettings, Field

class Base(BaseSettings):
    class Config:
        case_sensitive = False

    ENV: str = Field(..., env="FILE_HOLDER_ENV")

    # Application
    DEBUG: bool
    TITLE: str = "FILE HOLDER APP"
    UPLOAD_FOLDER: str
    HASH_ALGORITM: str = "md5"
    SECRET_KEY: str
    
    # Database
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_SYNC_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_ASYNC_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def BASE_DIR(self) -> Path:
        return Path().resolve()

class Local(Base):
    # Application
    
    UPLOAD_FOLDER: str
    DEBUG: bool = True
    HASH_ALGORITM: str = "md5"

     # Database
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        env_file = "local.env"

class Dev(Base):
    # Application
    DEBUG: bool = True
    UPLOAD_FOLDER: str

    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int = 5432

    class Config:
        env_file = "dev.env"

class Test(Base):
    # Application
    DEBUG: bool = False
    UPLOAD_FOLDER: str

    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int = 5432

    class Config:
        env_file = "test.env"

class Prod(Base):
    # Application
    DEBUG: bool = True
    UPLOAD_FOLDER: str

    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int = 5432

    class Config:
        env_file = "prod.env"


config_map = dict(
    local=Local,
    dev=Dev,
    test=Test,
    prod=Prod,
)


env_variable = os.environ.get("FILE_HOLDER_ENV")
if env_variable is None:
    raise ValueError("Not found 'FILE_HOLDER_ENV' environment variable")
env_variable = env_variable.lower()
if env_variable not in config_map.keys():
    raise ValueError(
        f"Incorrect 'FILE_HOLDER_ENV' environment variable, must be in {list(config_map.keys())}"
    )  # noqa: E501

try:
    settings: Base = config_map[env_variable]()  # type: ignore
except ValueError as e:
    print(f"Error on validate configuration from *.env: {e}")
    raise

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import BaseModel, PostgresDsn, Field

load_dotenv()


class RunSettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiPrefixSettings(BaseModel):
    prefix: str = "/api"


class DBSettings(BaseModel):
    url: PostgresDsn = os.getenv("DATABASE_URL")
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class OMDBsettings(BaseModel):
    api_key: str = os.getenv("OMDB_API_KEY")


class Settings(BaseSettings):
    run: RunSettings = RunSettings()
    api_prefix: ApiPrefixSettings = ApiPrefixSettings()
    db: DBSettings = DBSettings()
    omdb: OMDBsettings = OMDBsettings()


settings = Settings()

from pydantic_settings import BaseSettings
from pydantic import BaseModel


class RunSettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiPrefixSettings(BaseModel):
    prefix: str = "/api"


class Settings(BaseSettings):
    run: RunSettings = RunSettings()
    api_prefix: ApiPrefixSettings = ApiPrefixSettings()


settings = Settings()

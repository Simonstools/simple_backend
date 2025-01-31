from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding="utf-8", extra="ignore")

class JsonBinSettings(EnvBaseSettings):
    JSONBIN_API_KEY: str
    JSONBIN_ROOT_URL: str

class Settings(JsonBinSettings):
    pass

settings = Settings()

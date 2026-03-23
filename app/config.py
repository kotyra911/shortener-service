import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

lg = logging.getLogger()

load_dotenv()

class Settings(BaseSettings):

    MODE: str

    #db
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    #app
    BASE_URL: str

    @property
    def DB_URL(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()




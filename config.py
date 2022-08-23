from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    API_SECRET_KEY: str
    API_ALGORITHM: str

    class Config:
        env_file = '.env'

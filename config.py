from pydantic import BaseSettings

"""
Configuration file to communicate with Environment variable sin .env file
"""


class Settings(BaseSettings):
    DB_URL: str
    API_SECRET_KEY: str
    API_ALGORITHM: str

    class Config:
        env_file = '.env'

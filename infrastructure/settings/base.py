from typing import Optional
from pydantic import BaseSettings


class ApplicationSettings(BaseSettings):
    API_MULTI_URL: str
    API_SINGLE_URL: str
    STATIC_DIRECTORY: str
    STARTUP_MIGRATION: Optional[bool] = False

    class Config:
        extra = "ignore"

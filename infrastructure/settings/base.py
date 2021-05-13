from pydantic import BaseSettings


class ApplicationSettings(BaseSettings):
    API_MULTI_URL: str
    API_SINGLE_URL: str
    STATIC_DIRECTORY: str

    class Config:
        extra = "ignore"

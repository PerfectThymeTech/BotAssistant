import logging

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # General config
    PROJECT_NAME: str = "VideoAnalyzer"
    SERVER_NAME: str = "VideoAnalyzer"
    APP_VERSION: str = "v0.0.1"
    WEBSITE_NAME: str = Field(default="test", alias="WEBSITE_SITE_NAME")
    WEBSITE_INSTANCE_ID: str = Field(default="0", alias="WEBSITE_INSTANCE_ID")
    HOME_DIRECTORY: str = Field(default="", alias="HOME")

    # Identity settings
    MANAGED_IDENTITY_CLIENT_ID: str

    # Logging settings
    LOGGING_LEVEL: int = logging.INFO
    DEBUG: bool = False
    APPLICATIONINSIGHTS_CONNECTION_STRING: str = Field(
        default="", alias="APPLICATIONINSIGHTS_CONNECTION_STRING"
    )


settings = Settings()

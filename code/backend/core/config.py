import logging

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # General project settings
    PROJECT_NAME: str = "BotAssistantSample"
    SERVER_NAME: str = "BotAssistantSample"
    APP_VERSION: str = "v0.0.1"
    PORT: int = 8000

    # Web app settings
    WEBSITE_NAME: str = Field(default="test", alias="WEBSITE_SITE_NAME")
    WEBSITE_INSTANCE_ID: str = Field(default="0", alias="WEBSITE_INSTANCE_ID")
    HOME_DIRECTORY: str = Field(default="", alias="HOME")

    # Logging settings
    LOGGING_LEVEL: int = logging.INFO
    DEBUG: bool = False
    APPLICATIONINSIGHTS_CONNECTION_STRING: str = Field(
        default="", alias="APPLICATIONINSIGHTS_CONNECTION_STRING"
    )

    # Authentication settings
    APP_ID: str = Field(default="", alias="MICROSOFT_APP_ID")
    APP_PASSWORD: str = Field(default="", alias="MICROSOFT_APP_PASSWORD")
    APP_TENANTID: str = Field(default="", alias="MICROSOFT_APP_TENANTID")
    APP_TYPE: str = Field(default="", alias="MICROSOFT_APP_TYPE")
    MANAGED_IDENTITY_CLIENT_ID: str

    # Azure Open AI settings
    AZURE_OPEN_AI_ENDPOINT: str
    AZURE_OPEN_AI_API_VERSION: str = "2024-05-01-preview"
    AZURE_OPENAI_SYSTEM_PROMPT: str
    AZURE_OPENAI_MODEL_NAME: str
    AZURE_OPENAI_ASSISTANT_ID: str


settings = Settings()

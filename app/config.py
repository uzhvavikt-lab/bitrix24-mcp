import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки приложения.
    """

    # Настройки Bitrix24
    BITRIX_WEBHOOK_URL: str = os.getenv(
        "BITRIX_WEBHOOK_URL",
        "https://your-domain.bitrix24.ru/rest/1/yoursecretcode/",
    )

    # Настройки MCP-сервера
    MCP_HOST: str = os.getenv("MCP_HOST", "localhost")
    MCP_PORT: int = int(os.getenv("MCP_PORT", "8000"))

    # Другие настройки
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"


settings = Settings()

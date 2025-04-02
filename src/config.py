from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки приложения.
    """

    # Настройки Bitrix24
    BITRIX_WEBHOOK_URL: str = Field(
        "https://your-domain.bitrix24.ru/rest/1/yoursecretcode/",
    )

    # Другие настройки
    LOG_LEVEL: str = Field("INFO")

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore[call-arg]

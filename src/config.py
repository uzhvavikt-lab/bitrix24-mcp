"""Модуль конфигурации приложения.

Предоставляет настройки приложения через параметры командной строки.
"""

import typing
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения."""

    BITRIX_WEBHOOK_URL: str = Field(
        description="URL вебхука Bitrix24",
    )

    LOG_LEVEL: str = Field(
        default="INFO",
        description="Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    model_config = SettingsConfigDict(env_file=None)


class SettingsManager:
    """Менеджер настроек приложения.
    Реализует паттерн Singleton для управления настройками.
    """

    _instance: ClassVar[Settings | None] = None

    @classmethod
    def init(cls, **kwargs: typing.Any) -> Settings:
        """Инициализация настроек приложения.

        :param kwargs: Параметры конфигурации
        :return: Экземпляр настроек
        """
        cls._instance = Settings(**kwargs)
        return cls._instance

    @classmethod
    def get(cls) -> Settings:
        """Получение текущих настроек приложения.

        :return: Экземпляр настроек
        :raises RuntimeError: Если настройки не были инициализированы
        """
        if cls._instance is None:
            msg = (
                "Настройки не инициализированы. "
                "Вызовите SettingsManager.init() перед использованием."
            )
            raise RuntimeError(
                msg,
            )
        return cls._instance

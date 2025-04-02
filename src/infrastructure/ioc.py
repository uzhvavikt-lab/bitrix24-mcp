"""
Модуль с контейнером зависимостей приложения.

Предоставляет единую точку инициализации и получения зависимостей.
"""

from src import application
from src.config import settings
from wireup import create_container

from .bitrix import repository_factory
from .mcp import server

container = create_container(
    parameters={"bitrix_webhook_url": settings.BITRIX_WEBHOOK_URL},
    service_modules=[server, repository_factory, application],
)

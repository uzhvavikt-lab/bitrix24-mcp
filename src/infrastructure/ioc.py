"""Модуль с контейнером зависимостей приложения.

Предоставляет единую точку инициализации и получения зависимостей.
"""

from dishka import Provider, Scope, make_container, provide
from fast_bitrix24 import Bitrix

from src.config import SettingsManager
from src.infrastructure.bitrix.bitrix_contact_repository import (
    BitrixContactRepository,
)
from src.infrastructure.bitrix.bitrix_deal_repository import (
    BitrixDealRepository,
)
from src.infrastructure.bitrix.repository_factory import BitrixRepositoryFactory
from src.infrastructure.logging.logger import logger
from src.infrastructure.mcp.server import BitrixMCPServer


class AppProvider(Provider):
    """Основной провайдер приложения, объединяющий все зависимости."""

    def __init__(self) -> None:
        super().__init__()
        self.bitrix_webhook_url = SettingsManager.get().BITRIX_WEBHOOK_URL

    @provide(scope=Scope.APP)
    def provide_bitrix_webhook_url(self) -> str:
        """Предоставляет URL вебхука Bitrix."""
        return self.bitrix_webhook_url

    @provide(scope=Scope.APP)
    async def provide_repository_factory(
        self,
        bitrix_webhook_url: str,
    ) -> BitrixRepositoryFactory:
        """Создание фабрики репозиториев Bitrix24.

        :param bitrix_webhook_url: URL вебхука Bitrix24
        :return: Экземпляр фабрики репозиториев
        """
        bitrix_client = Bitrix(bitrix_webhook_url)
        logger.info("Инициализация фабрики репозиториев Bitrix24")
        contact_repository = BitrixContactRepository(bitrix_client)
        return BitrixRepositoryFactory(
            [
                contact_repository,
                BitrixDealRepository(bitrix_client, contact_repository),
            ],
        )

    @provide(scope=Scope.APP)
    def provide_mcp_server(self) -> BitrixMCPServer:
        """Предоставляет сервер MCP."""
        return BitrixMCPServer()


provider = AppProvider()
container = make_container(provider)

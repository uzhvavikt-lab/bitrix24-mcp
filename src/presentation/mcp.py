"""
Модуль с презентационным слоем MCP сервера.

Отвечает за конфигурацию и запуск MCP сервера для Bitrix24.
"""

from src.infrastructure.ioc import container
from src.infrastructure.mcp.handlers import (
    register_contact_handlers,
    register_deal_handlers,
)
from src.infrastructure.mcp.server import BitrixMCPServer
from mcp.server.fastmcp import FastMCP


@container.autowire
def create_mcp_server(mcp_server: BitrixMCPServer) -> FastMCP:
    """
    Создание и настройка MCP сервера для Bitrix24.

    Регистрирует все обработчики, промпты и инструменты.

    :return: Настроенный экземпляр MCP сервера
    """
    register_contact_handlers(mcp_server)
    register_deal_handlers(mcp_server)

    return mcp_server.server


server = create_mcp_server()


def main() -> None:
    """
    Точка входа для запуска MCP сервера.

    Эта функция вызывает метод ``run()`` на предварительно
    сконфигурированном экземпляре сервера ``FastMCP``,
    запуская его для обработки входящих запросов.
    """
    server.run()

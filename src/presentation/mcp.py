"""Модуль с презентационным слоем MCP сервера.

Отвечает за конфигурацию и запуск MCP сервера для Bitrix24.
"""

from argparse import ArgumentParser

from mcp.server.fastmcp import FastMCP

from src.config import SettingsManager
from src.infrastructure.ioc import container
from src.infrastructure.logging.logger import configure_log_level, logger
from src.infrastructure.mcp.handlers import (
    register_contact_handlers,
    register_deal_handlers,
)
from src.infrastructure.mcp.server import BitrixMCPServer


@container.autowire
def create_mcp_server(mcp_server: BitrixMCPServer) -> FastMCP:
    """Создание и настройка MCP сервера для Bitrix24.

    Регистрирует все обработчики, промпты и инструменты.

    :return: Настроенный экземпляр MCP сервера
    """
    register_contact_handlers(mcp_server)
    register_deal_handlers(mcp_server)

    return mcp_server.server


def parse_args() -> tuple[str, str]:
    """Парсинг аргументов командной строки.

    :return: Кортеж (webhook_url, log_level)
    :raises SystemExit: Если не указаны обязательные аргументы
    """
    parser = ArgumentParser(description="Bitrix24 MCP Server")
    parser.add_argument(
        "--bitrix-webhook-url",
        required=True,
        help="URL вебхука Bitrix24",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Уровень логирования",
    )

    args = parser.parse_args()
    return args.bitrix_webhook_url, args.log_level.upper()


def main() -> None:
    """Точка входа для запуска MCP сервера.

    Эта функция инициализирует настройки и запускает MCP сервер
    для обработки входящих запросов.
    """
    webhook_url, log_level = parse_args()

    SettingsManager.init(
        BITRIX_WEBHOOK_URL=webhook_url,
        LOG_LEVEL=log_level,
    )
    configure_log_level(log_level)

    logger.info("Запуск MCP сервера")

    server = create_mcp_server()
    server.run()


if __name__ == "__main__":
    main()

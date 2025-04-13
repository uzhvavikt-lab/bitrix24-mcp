"""Модуль для централизованной настройки логирования с использованием structlog.

Предоставляет структурированное логирование для всего приложения.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import structlog


def _configure_logging() -> structlog.stdlib.BoundLogger:
    """Настройка системы логирования.

    :returns: Настроенный structlog логгер
    """
    logging.getLogger("fast_bitrix24").setLevel(logging.WARNING)

    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
        handlers=[],
    )

    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    log_file = Path("logs/app.log")
    log_dir = log_file.parent

    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
    )
    root_logger.addHandler(file_handler)

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    structlog.configure(
        processors=[*processors, structlog.dev.ConsoleRenderer()],
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


logger = _configure_logging()


def configure_log_level(level: str) -> None:
    """Настройка уровня логирования.

    :param level: Уровень логирования
    """
    logging.getLogger().setLevel(level)

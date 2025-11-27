"""Настройка и конфигурация логирования для проекта.

Предоставляет централизованное управление логированием с поддержкой
различных уровней логов и форматирования.
"""

import logging
import sys
from typing import Optional



def setup_logging(level: int = logging.INFO) -> None:
    """
    ## Настраивает базовое логирование для всего приложения.

    Args:
        level: Уровень логирования (logging.DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    # Формат логов
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # Настройка базового логгера
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Отключаем избыточное логирование SQLAlchemy
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    ## Возвращает настроенный логгер для модуля.

    Args:
        name: Имя логгера (обычно __name__ модуля). Если None, возвращает root logger.

    Returns:
        logging.Logger: Настроенный экземпляр логгера.

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Сообщение в лог")
    """
    if name is None:
        return logging.getLogger()
    return logging.getLogger(name)



# Публичный API модуля
__all__ = ['get_logger', 'setup_logging']
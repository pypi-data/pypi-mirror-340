import os
import sys

from dotenv import load_dotenv, find_dotenv
from loguru import logger as log

from .helpers.constants import DEFAULT_LOG_LEVEL, ENV_LEVEL_NAME


def add_stdout():
    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        load_dotenv(dotenv_path=dotenv_path, override=True)

    log.add(
        sys.stdout,  # Приемник - стандартный вывод
        level=os.environ.get(ENV_LEVEL_NAME, DEFAULT_LOG_LEVEL).upper(),
        colorize=True,  # Включить цвета
        backtrace=True,  # Всегда включать подробный стектрейс (если есть)
        diagnose=True,  # Включать значения переменных в стектрейс (может быть медленно)
        format="<blue>{time:HH:mm:ss}</blue> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>"
    )


def add_serialize():
    # Структурированное логирование (JSON) - ИДЕАЛЬНО для Docker и систем агрегации:
    log.add(
        sys.stderr,  # Вывод в stderr (стандарт для Docker)
        level="TRACE",
        serialize=True  # Вывод в формате JSON
    )


def log_test():
    log.trace("Это сообщение для отладки (по умолчанию не видно)")
    log.debug("Это сообщение для отладки (по умолчанию не видно)")
    log.info("Какая-то информационная заметка")
    log.warning("Предупреждение, что-то может пойти не так")
    log.error("Произошла ошибка, но программа может продолжать работу")
    log.critical("Критическая ошибка, программа, скорее всего, упадет")

    try:
        variable = 0
        result = 1 / variable
    except ZeroDivisionError:
        log.exception("Произошло исключение!")  # Автоматически добавит стектрейс


# Переменная LOG_LEVEL может быть установлена в .env файле или в системе
log.remove()
add_stdout()

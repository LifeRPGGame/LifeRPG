import asyncio

import pytz
import logging
from datetime import datetime

import requests
from inspect import stack, getmodule

from utils.config import BOT_KEY, MODERATOR_ID


class BotLogger:
    def __init__(self, file: str = 'main.log') -> None:
        """
        Общий класс для логгирования действия внутри бота.

        Логгирует в файл с именем файла, откуда был вызван.

        Использование:
        1. Импортировать класс с указанием имени файла для логов, например users.log
        2. Логи будут записаны с указанием модуля, откуда был вызван класс.
        """
        # Получение информации о файле вызова
        frame = stack()[1]
        module = getmodule(frame[0])
        name = module.__file__.split('/')[-1] if module else __name__

        # Настройка логгера
        self.logger = logging.getLogger(name)

        # Если у логгера уже есть обработчики, не добавляем их снова
        if not self.logger.hasHandlers():
            # Создаем обработчик для записи в файл
            file_handler = logging.FileHandler(file)
            file_handler.setLevel(logging.INFO)

            # Настройка форматтера с временной зоной UTC+3
            formatter = logging.Formatter(
                fmt=f'%(levelname)s - {name} - %(asctime)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)

            # Добавляем обработчик к логгеру
            self.logger.addHandler(file_handler)
            self.logger.setLevel(logging.INFO)

        logging.getLogger('aiogram').setLevel(logging.WARNING)

    def formatTime(self, record, datefmt=None):
        """Переопределение метода форматирования времени с учетом UTC+3."""
        # Получение текущего времени с учетом временной зоны
        tz = pytz.timezone('Europe/Moscow')  # UTC+3
        record_time = datetime.fromtimestamp(record.created, tz)
        if datefmt:
            return record_time.strftime(datefmt)
        else:
            return record_time.isoformat()

    async def send_alert(self, text: str) -> None:
        url = f'https://api.telegram.org/bot{BOT_KEY}/sendMessage'
        params = {
            'chat_id': MODERATOR_ID,
            'text': f'СООБЩЕНИЕ ОТ БОТА:\n{text}'}
        requests.post(url, params=params)

    async def info(self, message: str, send_alert: bool = False, extra: dict = None) -> None:
        if send_alert:
            await self.send_alert(text=message)
        self.logger.info(msg=message, extra=extra)

    async def error(self, message: str) -> None:
        self.logger.error(message)
        await self.send_alert(text=message)

    async def critical(self, message: str, extra: dict = None) -> None:
        await asyncio.sleep(2)
        self.logger.critical(message, extra=extra)
        await self.send_alert(text=f'{message}\nExtra:{extra}')
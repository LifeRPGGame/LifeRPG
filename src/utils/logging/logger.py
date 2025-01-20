from logtail import LogtailHandler
import logging
import requests
from utils.config import LOG_TOKEN
from utils.config import BOT_KEY
from utils.config import MODERATOR_ID


class NotModeratorId(Exception):
    pass


class MyLogger():
    def __init__(self) -> None:
        handler = LogtailHandler(source_token=LOG_TOKEN)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.handlers = []
        logger.addHandler(handler)
        self.logger = logger

    async def send_alert_to_main_moderator(self, text: str) -> None:
        if MODERATOR_ID != '':
            url = f'https://api.telegram.org/bot{BOT_KEY}/sendMessage'
            params = {
                'chat_id': MODERATOR_ID,
                'text': f'СООБЩЕНИЕ ОТ БОТА:\n{text}'}
            requests.post(url, params=params)
        else:
            raise NotModeratorId('MODERATOR_ID is not set')

    async def info(self, message: str, send_alert: bool = False, extra: dict = None) -> None:
        print(f'send_alert_to_main_moderator: {message}, LOG_TOKEN: {LOG_TOKEN}')
        if LOG_TOKEN == '':
            self.logger.info(message)
            return await self.send_alert_to_main_moderator(text=message)
        else:         
            if send_alert:
                await self.send_alert_to_main_moderator(text=message)
                self.logger.info(msg=message, extra=extra)
            else:
                self.logger.info(message)

    async def error(self, message: str) -> None:
        if LOG_TOKEN == '':
            print(f'send_alert_to_main_moderator: {message}')
        else: 
            self.logger.error(message)
            await self.send_alert_to_main_moderator(
                text=message
            )
        
    async def critical(self, message: str, extra: dict = None) -> None:
        if LOG_TOKEN == '':
            print(f'send_alert_to_main_moderator: {message}')
        else: 
            self.logger.critical(message, extra=extra)
            await self.send_alert_to_main_moderator(
                text=f'{message}\nEXtra:{extra}')
    

logger = MyLogger()

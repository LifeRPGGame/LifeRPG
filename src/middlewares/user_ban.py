from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

from utils.db.user import *
from utils.logging.logger import logger

import asyncio


class CheckUserWasBannedMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:
        user_id = event.from_user.id
        if await UserOrm().is_banned_user(user_id=user_id):
            # passing if user is banned
            pass

        else:
            return await handler(event, data)

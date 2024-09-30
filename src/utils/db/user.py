import sqlalchemy
import datetime
from typing import Union
from sqlalchemy import select, update, func, delete
from pydantic import BaseModel

from . import async_session
from utils.db.models import *
from utils.logging.logger import logger


class User(BaseModel):
    user_id: int
    username: str
    full_name: str
    join_time: datetime.datetime
    is_banned: bool
    welcome_notif_id: int   
    feature_notif_id: int
    hearts: int
    power: int
    money: float
    level: int
    max_hearts: int
    max_power: int


class UserOrm:
    async def is_banned_user(self, user_id: int) -> bool:
        try:
            async with async_session() as session:
                query = select(UserModel.is_banned).where(
                    UserModel.user_id == user_id)
                result = await session.execute(query)
                banned = result.scalars().first()
                if banned:
                    return True
                return False
        except TypeError:
            return False

    async def add(
        self,
        user_id: int,
        username: int | None,
        full_name: str,
    ):
        async with async_session() as session:
            async with session.begin():
                try:
                    session.add(UserModel(
                        user_id=user_id,
                        username=username,
                        full_name=full_name,
                        join_time=datetime.datetime.now()
                    ))
                    await session.commit()
                except sqlalchemy.exc.IntegrityError:
                    pass
            
    async def get(self, user_id: int) -> User:
        async with async_session() as session:
            query = select(UserModel).where(UserModel.user_id == user_id)
            result = await session.execute(query)
            for i in result:
                return User(
                    user_id=i.UserModel.user_id,
                    username=i.UserModel.username,
                    full_name=i.UserModel.full_name,
                    join_time=i.UserModel.join_time,
                    is_banned=i.UserModel.is_banned,
                    welcome_notif_id=i.UserModel.welcome_notif_id,
                    feature_notif_id=i.UserModel.feature_notif_id,
                    hearts=i.UserModel.hearts,
                    power=i.UserModel.power,
                    money=i.UserModel.money,
                    level=i.UserModel.level,
                    max_hearts=i.UserModel.max_hearts,
                    max_power=i.UserModel.max_power
                )

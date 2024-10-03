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
    money: int
    experience: int
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
                    experience=i.UserModel.experience,
                    level=i.UserModel.level,
                    max_hearts=i.UserModel.max_hearts,
                    max_power=i.UserModel.max_power
                )

    async def plus_value(
            self,
            user_id: int,
            hearts: int = None,
            power: int = None,
            money: int = None,
            experience: int = None,
            level: int = None,
            max_hearts: int = None,
            max_power: int = None
        ) -> None:
        async with async_session() as session:
            async with session.begin():
                # Создаем словарь для обновляемых значений
                old_user_data = await self.get(user_id=user_id)
                update_values = {}
                if hearts is not None:
                    update_values['hearts'] = hearts + old_user_data.hearts
                if power is not None:
                    update_values['power'] = power + old_user_data.power
                if money is not None:
                    update_values['money'] = money + old_user_data.money
                if experience is not None:
                    update_values['experience'] = experience + old_user_data.experience
                if level is not None:
                    update_values['level'] = level + old_user_data.level
                if max_hearts is not None:
                    update_values['max_hearts'] = max_hearts + old_user_data.max_hearts
                if max_power is not None:
                    update_values['max_power'] = max_power + old_user_data.max_power

                # Выполняем обновление только если есть значения для обновления
                if update_values:
                    query = update(UserModel).where(
                        UserModel.user_id == user_id
                    ).values(**update_values)
                    await session.execute(query)


import sqlalchemy
import datetime
from typing import Optional, Literal
from sqlalchemy import select, update, func, delete
from pydantic import BaseModel
from random import randint

from . import async_session
from utils.logging.logger import logger
from utils.db.models import *
from utils.db.user import UserOrm
from utils.db.item import ItemOrm

from utils.config import get_inventory_count_for_level
from utils.exceptions import *


class InventoryItem(BaseModel):
	id: int
	hash_id: int
	user_id: int
	item_id: int
	is_clothed: bool  # надета ли одежда
	is_weaponed: bool  # надето ли оружие


async def generate_inventory_item_hash_id() -> int:
	return randint(100000, 999999)


class InventoryOrm:
	async def add_to_inventory(
			self, user_id: int, item_id: int
	) -> None:
		async with async_session() as session:
			async with session.begin():
				print('начало добавления в инвентарь...')

				item = await ItemOrm().get(item_id=item_id)
				count_of_type = len(await self.get_inventory_of_type(user_id=user_id, type=item.type))
				print(f'количества предметов до добавления: {count_of_type}')

				user = await UserOrm().get(user_id=user_id)
				max_inventory_count = await get_inventory_count_for_level(level=user.level)
				print(f'макс кол-во предметов для уровня пользователя: {max_inventory_count}')

				if count_of_type >= max_inventory_count:
					raise UserInventoryIsFull()

				session.add(
					InventoryModel(
						hash_id=await generate_inventory_item_hash_id(),
						user_id=user_id,
						item_id=item_id,
					)
				)
				await session.commit()

	async def remove_from_inventory(
			self, user_id: int, hash_id: int
	) -> None:
		async with async_session() as session:
			async with session.begin():
				query = delete(InventoryModel).where(
					(InventoryModel.user_id == user_id) &
					(InventoryModel.hash_id == hash_id)
				)
				await session.execute(query)
				await session.commit()

	async def get_inventory(self, user_id: int) -> list[InventoryItem]:
		async with async_session() as session:
			async with session.begin():
				query = select(InventoryModel).where(
					InventoryModel.user_id == user_id
				)
				inventory = []

				result = await session.execute(query)
				for i in result:
					inventory.append(
						InventoryItem(
							id=i.InventoryModel.id,
							hash_id=i.InventoryModel.hash_id,
							user_id=i.InventoryModel.user_id,
							item_id=i.InventoryModel.item_id,
							is_clothed=i.InventoryModel.is_clothed,
							is_weaponed=i.InventoryModel.is_weaponed,
						)
					)
				return inventory

	async def item_in_inventory(self, user_id: int, hash_id: int = None, item_id: int = None) -> bool:
		"""
		Возвращает True, если предмет известен(в инвентаре)
		:param user_id: идентификатор пользователя
		:param hash_id: ID предмета в инвентаре пользователя
		:param item_id: ID предмета в игре
		"""

		async with async_session() as session:
			async with session.begin():
				if hash_id:
					query = select(InventoryModel).where(
						(InventoryModel.user_id == user_id) &
						(InventoryModel.hash_id == hash_id)
					)
				else:
					query = select(InventoryModel).where(
						(InventoryModel.user_id == user_id) &
						(InventoryModel.item_id == item_id)
					)
				result = await session.execute(query)
				item = result.scalars().first()

				return item is not None

	async def get_inventory_of_type(
			self,
			user_id: int,
			type: str
	) -> list[InventoryItem]:
		async with async_session() as session:
			async with session.begin():
				query = select(InventoryModel).where(InventoryModel.user_id == user_id)
				res = []
				result = await session.execute(query)
				for i in result:
					item = await ItemOrm().get(item_id=i.InventoryModel.item_id)  # Получаем item через ORM
					if getattr(item, 'type') == type:  # Проверяем тип через объект item
						res.append(
							InventoryItem(
								id=i.InventoryModel.id,
								hash_id=i.InventoryModel.hash_id,
								user_id=i.InventoryModel.user_id,
								item_id=i.InventoryModel.item_id,
								is_clothed=i.InventoryModel.is_clothed,
								is_weaponed=i.InventoryModel.is_weaponed,
							)
						)
				return res

	async def get_inventory_item(self, hash_id: int) -> InventoryItem:
		async with async_session() as session:
			async with session.begin():
				query = select(InventoryModel).where(InventoryModel.hash_id == hash_id)
				result = await session.execute(query)
				for i in result.mappings():
					return InventoryItem(
						id=i.InventoryModel.id,
						hash_id=i.InventoryModel.hash_id,
						user_id=i.InventoryModel.user_id,
						item_id=i.InventoryModel.item_id,
						is_clothed=i.InventoryModel.is_clothed,
						is_weaponed=i.InventoryModel.is_weaponed,
					)


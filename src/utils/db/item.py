import sqlalchemy
import datetime
from typing import Optional
from typing import Union
from sqlalchemy import select, update, func, delete
from pydantic import BaseModel

from . import async_session
from utils.db.models import *
from utils.logging.logger import logger


class Item(BaseModel):
	id: int
	type: str
	name: str
	description: str
	price: float
	damage: Optional[float] = None  # for weapons
	heal: Optional[float] = None  # for foods and poisons


class ItemOrm:
	async def get(self, item_id: int) -> Item:
		"""
		Получение предмета по его ID

		Parameters:
			item_id: int
		Returns:
			Item
		"""

		async with async_session() as session:
			async with session.begin():
				query = select(ItemModel).where(ItemModel.id == item_id)
				for i in await session.execute(query):
					return Item(
						id=i.ItemModel.id,
						type=i.ItemModel.type,
						name=i.ItemModel.name,
						description=i.ItemModel.description,
						price=i.ItemModel.price,
						damage=i.ItemModel.damage,
						heal=i.ItemModel.heal,
					)
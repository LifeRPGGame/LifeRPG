import sqlalchemy
import datetime
from typing import Union
from sqlalchemy import select, update, func, delete
from pydantic import BaseModel

from . import async_session
from utils.db.models import *


class Location(BaseModel):
	id: int
	user_id: int
	name: str


class LocationOrm:
	"""
	Класс для взаимодействия с локациями пользователя через ORM
	"""

	async def get_user_locations(
			self,
			user_id: int
	) -> list[Location]:
		async with async_session() as session:
			async with session.begin():
				query = select(
					LocationModel
				).where(
					LocationModel.user_id == user_id
				)
				res = []
				for l in await session.execute(query):
					res.append(
						Location(
							id=l.LocationModel.id,
							user_id=l.LocationModel.user_id,
							name=l.LocationModel.name
						)
					)
				return res

	async def add(
			self,
			user_id: int,
			name: str
	):
		async with async_session() as session:
			async with session.begin():
				session.add(
					LocationModel(
						user_id=user_id,
						name=name
					)
				)
				await session.commit()

	async def get_by_id(self, location_id: int) -> Location:
		async with async_session() as session:
			async with session.begin():
				query = select(
					LocationModel
				).where(LocationModel.id == location_id)
				for i in await session.execute(query):
					return Location(
						id=i.LocationModel.id,
						user_id=i.LocationModel.user_id,
						name=i.LocationModel.name
					)

	async def delete(self, location_id: int) -> None:
		async with async_session() as session:
			async with session.begin():
				query = delete(LocationModel).where(LocationModel.id == location_id)
				await session.execute(query)
				await session.commit()

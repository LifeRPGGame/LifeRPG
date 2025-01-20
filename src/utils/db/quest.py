import sqlalchemy
import datetime
import pytz
from typing import Union
from sqlalchemy import select, update, func, delete
from pydantic import BaseModel

from . import async_session
from utils.db.models import *
from utils.config import MY_TIMEZONE


class Quest(BaseModel):
	id: int
	location_id: int
	user_id: int
	name: str
	type: str
	benefits: str
	add_time: datetime.datetime


class QuestOrm:
	async def get_quests(self, user_id: int) -> list[Quest]:
		async with async_session() as session:
			async with session.begin():
				query = select(Quest).where(QuestModel.user_id == user_id)
				res = []
				for q in await session.execute(query):
					res.append(
						Quest(
							id=q.QuestModel.id,
							location_id=q.QuestModel.location_id,
							user_id=q.QuestModel.user_id,
							name=q.QuestModel.name,
							add_time=q.QuestModel.add_time.astimezone(MY_TIMEZONE)
						)
					)
				return res

	async def add(self, user_id: int, name: str, location_id: int, type: str, benefits: str) -> None:
		async with async_session() as session:
			async with session.begin():
				session.add(
					QuestModel(
						user_id=user_id,
						name=name,
						type=type,
						location_id=location_id,
						benefits=benefits,
						add_time=datetime.datetime.now(MY_TIMEZONE)
					)
				)
				await session.commit()

	async def delete(self, quest_id: int) -> bool:
		async with async_session() as session:
			async with session.begin():
				query = delete(
							QuestModel
						).where(
							QuestModel.id == quest_id
				)
				await session.execute(query)
				await session.commit()

	async def get_location_quests(self, location_id: int) -> list[Quest]:
		async with async_session() as session:
			async with session.begin():
				query = select(QuestModel).where(QuestModel.location_id == location_id)
				res = []
				for q in await session.execute(query):
					res.append(
						Quest(
							id=q.QuestModel.id,
							location_id=q.QuestModel.location_id,
							name=q.QuestModel.name,
							user_id=q.QuestModel.user_id,
							type=q.QuestModel.type,
							benefits=q.QuestModel.benefits,
							add_time=q.QuestModel.add_time.astimezone(MY_TIMEZONE)
						)
					)
				return res

	async def get_quest(self, quest_id: int) -> Quest:
		async with async_session() as session:
			async with session.begin():
				query = select(QuestModel).where(QuestModel.id == quest_id)
				for q in await session.execute(query):
					return Quest(
						id=q.QuestModel.id,
						location_id=q.QuestModel.location_id,
						name=q.QuestModel.name,
						user_id=q.QuestModel.user_id,
						type=q.QuestModel.type,
						benefits=q.QuestModel.benefits,
						add_time=q.QuestModel.add_time.astimezone(MY_TIMEZONE)
					)

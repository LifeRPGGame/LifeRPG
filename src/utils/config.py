import os
import pytz
import toml
from dotenv import load_dotenv

load_dotenv()

BOT_KEY = os.getenv('BOT_KEY')
LOG_TOKEN = os.getenv('LOG_TOKEN')
MODERATOR_ID = int(os.getenv('MODERATOR_ID'))
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_USER = os.getenv('POSTGRESQL_USER')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')
DSN = f'postgresql+asyncpg://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DBNAME}'

MY_TIMEZONE = pytz.timezone('Europe/Moscow')


async def get_quest_settings(quest_complexity: str) -> list:
	file = toml.load('default_settings.toml')
	quests = file['quests']
	for q in quests:
		if q['complexity'] == quest_complexity:
			return [q['complexity'], q['experience'], q['coins'], q['cooldown_mins']]

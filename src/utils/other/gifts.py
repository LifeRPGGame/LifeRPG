import aiogram

from . import *
from utils.config import MODERATOR_ID
from utils.db.inventory import InventoryOrm


class Gift:
	def __init__(self, bot: aiogram.Bot, dp: aiogram.Dispatcher):
		self.bot = bot
		self.dp = dp

	async def send_gift(self):
		await self.bot.send_message(
			chat_id=MODERATOR_ID,
			text=f'''
🎁 Вы получили подарок:
Apple x2

''')
		await InventoryOrm().add_to_inventory(
			user_id=MODERATOR_ID,
			item_id=1
		)
		await InventoryOrm().add_to_inventory(
			user_id=MODERATOR_ID,
			item_id=1
		)
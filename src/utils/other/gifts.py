import aiogram

from . import *
from utils.config import MODERATOR_ID
from utils.db.inventory import InventoryOrm

from utils.exceptions import *


class Gift:
	def __init__(self, bot: aiogram.Bot, dp: aiogram.Dispatcher):
		self.bot = bot
		self.dp = dp

	async def send_gift(self):
		await self.bot.send_message(
			chat_id=MODERATOR_ID,
			text=f'''
🎉 You got a gift:
Apple x2

''')
		try:
			await InventoryOrm().add_to_inventory(
				user_id=MODERATOR_ID,
				item_id=1
			)
		except UserInventoryIsFull:
			await self.bot.send_message(
				chat_id=MODERATOR_ID,
				text='Your inventory is full. You lost the gift: Apple'
			)
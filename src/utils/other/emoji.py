import aiogram
from aiogram import types
import  asyncio


async def send_emoji(
        callback: types.CallbackQuery = None,
        message: types.Message = None,
        bot: aiogram.Bot = None,
        emoji: str = '🧭',
        to_delete: bool = True,
        time: float = 2.5,
):
    """Отправка крутого эмодзи в чат"""
    
    if callback:
        emoji_message = await callback.message.answer(
            text=emoji
        )
        await asyncio.sleep(time)
        if to_delete:
            await emoji_message.delete()

    if bot:
        emoji_message = await bot.send_message(
            chat_id=message.chat.id,
            text=emoji
        )
        await asyncio.sleep(time)
        if to_delete:
            await emoji_message.delete()

    if message:
        emoji_message = await message.answer(
            text=emoji
        )
        await asyncio.sleep(time)
        if to_delete:
            await emoji_message.delete()

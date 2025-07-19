from aiogram import Bot
from config import CHANNEL_ID

async def send_post(bot: Bot, text: str):
    await bot.send_message(chat_id=CHANNEL_ID, text=text)
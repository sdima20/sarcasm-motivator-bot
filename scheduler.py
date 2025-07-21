from apscheduler.schedulers.asyncio import AsyncIOScheduler
from content.content_loader import get_random_post
from services.post_sender import send_post
from services.gemini_client import generate_sarcastic_post
from services.image_post_creator import create_image_post
from aiogram.types import FSInputFile
from aiogram import Bot
import asyncio
from config import BOT_TOKEN, CHANNEL_ID
from datetime import datetime

bot = Bot(token=BOT_TOKEN)
scheduler = AsyncIOScheduler()

def setup_schedule():
    scheduler.add_job(
        send_sarcastic_post,
        trigger='interval',
        minutes=15,
        next_run_time=datetime.now()
    )
    scheduler.start()

async def send_sarcastic_post():
    # 50/50: або з бази, або згенерувати
    from random import choice
    use_ai = choice([True, True])

    if use_ai:
        post = await generate_sarcastic_post()
        if not post:
            print("⚠️ GPT не згенерував. fallback -> база")
            post = get_random_post()
    else:
        post = get_random_post()

    #await send_post(bot, post)
    path = create_image_post(post)
    await bot.send_photo(CHANNEL_ID, photo=FSInputFile(path), caption="")
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from content.content_loader import get_random_post
from services.post_sender import send_post
from services.gemini_client import generate_sarcastic_post
from services.image_post_creator import create_image_post
from content.prompt_manager import get_current_prompt
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
    
    prompt = get_current_prompt()

    post = await generate_sarcastic_post(prompt=prompt)
    if not post:
        print("⚠️ GPT не згенерував. fallback -> база")
        post = get_random_post()

    #await send_post(bot, post)
    path = create_image_post(post)
    await bot.send_photo(CHANNEL_ID, photo=FSInputFile(path), caption="")

def setup_schedule():
    # Час публікацій у добі
    posting_hours = [8, 11, 14, 17, 21]  # 5 постів на день

    for hour in posting_hours:
        scheduler.add_job(
            lambda: asyncio.create_task(send_sarcastic_post()),
            trigger=CronTrigger(hour=hour, minute=0),
            name=f"Post at {hour}:00"
        )

    scheduler.start()
    print("🕒 Розклад публікацій запущено.")
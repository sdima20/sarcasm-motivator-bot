from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from content.content_loader import get_random_post
from services.post_sender import send_post
from services.gemini_client import generate_sarcastic_post
from services.image_post_creator import create_image_post
from content.prompt_manager import get_current_prompt
from aiogram.types import FSInputFile
from aiogram import Bot
from config import BOT_TOKEN, CHANNEL_ID
from datetime import datetime

scheduler = AsyncIOScheduler()

async def send_sarcastic_post():
    print(f"🟢 Виклик send_sarcastic_post() о {datetime.now()}")
    prompt = get_current_prompt()
    post = await generate_sarcastic_post(prompt=prompt)
    if not post:
        print("⚠️ GPT не згенерував. fallback -> база")
        post = get_random_post()
    path = create_image_post(post)
    bot = Bot(token=BOT_TOKEN)  # Створити бот тут або передати
    await bot.send_photo(CHANNEL_ID, photo=FSInputFile(path), caption="")
    await bot.session.close()
    print("✅ Пост відправлено")

async def setup_schedule():
    posting_hours = [8, 11, 14, 19, 21]
    for hour in posting_hours:
        scheduler.add_job(
            send_sarcastic_post,
            trigger=CronTrigger(hour=hour, minute=50),
            name=f"Post at {hour}:00"
        )
    scheduler.start()
    print("🕒 Розклад публікацій запущено.")
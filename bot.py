import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from scheduler import setup_schedule, send_sarcastic_post
from handlers import admin

bot = Bot(token=BOT_TOKEN)


async def main():
    dp = Dispatcher()
    dp.include_router(admin.router)
    await setup_schedule()
    print("🤖 Бот запущено.")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
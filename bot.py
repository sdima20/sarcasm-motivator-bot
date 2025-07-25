import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from scheduler import setup_schedule, send_sarcastic_post

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    setup_schedule()
    print("🤖 Бот запущено. Чекає на час посту...")

    # 🚀 Тестовий пост одразу при запуску
    #await send_sarcastic_post()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
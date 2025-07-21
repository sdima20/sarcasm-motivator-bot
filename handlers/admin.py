from aiogram import Router, F
from aiogram.types import Message
from config import ADMIN_ID  # Додай свій user_id в цей файл
from content.prompt_manager import update_prompt, load_prompts

router = Router()

@router.message(F.text.startswith("/set_prompt"))
async def set_prompt_command(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.reply("⛔ Лише для адміна")

    try:
        _, rest = message.text.split("/set_prompt", 1)
        key, value = rest.strip().split("|", 1)
        key = key.strip()
        value = value.strip()
        update_prompt(key, value)
        await message.reply(f"✅ Промпт '{key}' оновлено.")
    except Exception as e:
        await message.reply(f"⚠️ Помилка: {e}\nПриклад: /set_prompt image_prompt | Новий текст")

@router.message(F.text == "/get_prompt")
async def get_prompt(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Ти не адмін.")

    prompt = load_prompts()
    await message.answer(get_prompt("default"))
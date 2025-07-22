from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from content.prompt_manager import load_prompts, update_prompt, get_all_prompts, set_current_prompt
from config import ADMIN_ID

router = Router()

class AddPromptStates(StatesGroup):
    waiting_for_key = State()
    waiting_for_text = State()

@router.message(Command("add_prompt"))
async def cmd_add_prompt(message: Message, state: FSMContext):
    if str(message.from_user.id) != str(ADMIN_ID):
        await message.answer("❌ Ти не адмін.")
        return
    await message.answer("🔑 Введи новий ключ промпта:")
    await state.set_state(AddPromptStates.waiting_for_key)

@router.message(AddPromptStates.waiting_for_key)
async def add_prompt_get_key(message: Message, state: FSMContext):
    key = message.text.strip()
    prompts = load_prompts()

    if key in prompts:
        await message.answer(f"⚠️ Ключ `{key}` вже існує. Використай /set_prompt щоб змінити.")
        await state.clear()
        return

    await state.update_data(key=key)
    await message.answer("✍️ Введи текст нового промпта:")
    await state.set_state(AddPromptStates.waiting_for_text)

@router.message(AddPromptStates.waiting_for_text)
async def add_prompt_get_text(message: Message, state: FSMContext):
    data = await state.get_data()
    key = data["key"]
    new_prompt = message.text.strip()
    update_prompt(key, new_prompt)
    await message.answer(f"✅ Новий промпт з ключем `{key}` додано.")
    await state.clear()

@router.message(F.text.startswith("/set_prompt"))
async def handle_set_prompt(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Ти не адмін.")

    parts = message.text.strip().split(maxsplit=1)
    if len(parts) != 2:
        return await message.answer("❗ Вкажи ключ промпта, приклад:\n`/set_prompt monday`", parse_mode="Markdown")

    key = parts[1].strip()
    success = set_current_prompt(key)
    if success:
        await message.answer(f"✅ Промпт `{key}` встановлено як активний.", parse_mode="Markdown")
    else:
        await message.answer(f"⚠️ Промпт з ключем `{key}` не знайдено.", parse_mode="Markdown")

@router.message(F.text == "/get_prompt")
async def handle_get_prompt(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Ти не адмін.")

    prompt_list = get_all_prompts()
    await message.answer(prompt_list)
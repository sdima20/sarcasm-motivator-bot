import json
from pathlib import Path

PROMPTS_FILE = Path("content\prompts.json")

def load_prompts():
    with PROMPTS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def get_prompt(key: str) -> str:
    return load_prompts().get(key, "Промпт не знайдено.")

def update_prompt(key: str, new_prompt: str):
    prompts = load_prompts()
    prompts[key] = new_prompt
    with open(PROMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

def get_all_prompts() -> str:
    prompts = load_prompts()
    if not prompts:
        return "📭 Немає жодного промпта."

    result = "🧠 Доступні промпти:\n"
    for key in prompts:
        result += f"• {key}\n"
    return result

def set_current_prompt(key: str) -> bool:
    prompts = load_prompts()
    if key not in prompts:
        return False
    prompts["current"] = key
    with PROMPTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
    return True

def get_current_prompt() -> str:
    prompts = load_prompts()
    key = prompts.get("current", "default")
    return prompts.get(key, "Промпт не знайдено.")
import json

PROMPTS_FILE = "content\prompts.json"

def load_prompts():
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_prompt(key: str) -> str:
    return load_prompts().get(key, "")

def update_prompt(key: str, new_prompt: str):
    prompts = load_prompts()
    prompts[key] = new_prompt
    with open(PROMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
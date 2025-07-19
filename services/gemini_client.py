import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-pro")

async def generate_sarcastic_post():
    prompt = (
        "Згенеруй одну коротку саркастичну мотиваційну фразу українською мовою. "
        "Тон — мотиваційний, але з іронією або пасивною агресією. До 30 слів. Без пояснень."
    )

    try:
        # Gemini працює синхронно, тому використовуємо `run_in_executor`
        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
        return response.text.strip()
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return None

def list_models():
    models = genai.list_models()
    print("Available models:")
    for m in models:
        print(f"- {m.name}")

if __name__ == "__main__":
    list_models()
import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_sarcastic_post():
    prompt = (
        "Згенеруй одну коротку саркастичну мотиваційну фразу українською мовою. "
        "Стиль — злегка пасивно-агресивний, з іронією над сучасною псевдомотивацією. "
        "Фраза має бути не довша за 30 слів. Без пояснень."
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=60,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ OpenAI error: {e}")
        return None
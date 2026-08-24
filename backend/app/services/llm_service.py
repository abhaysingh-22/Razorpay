# pyrefly: ignore [missing-import]
from groq import Groq
from app.config import settings

client = Groq(api_key=settings.groq_api_key)

def call_llm(system_prompt: str, user_prompt: str, model: str = "openai/gpt-oss-120b") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,   # low temp — you want consistent, predictable decisions, not creativity
    )
    return response.choices[0].message.content
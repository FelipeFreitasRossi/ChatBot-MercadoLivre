import httpx
import asyncio
from app.core.config import settings

async def test_gemini():
    api_key = settings.gemini_api_key
    model = "gemini-3.6-flash"  # ou gemini-1.5-pro
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": "Qual o preço do smartphone?"}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 300}
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=30)
            print("Status:", response.status_code)
            print("Resposta:", response.text)
        except Exception as e:
            print("Erro:", e)

if __name__ == "__main__":
    asyncio.run(test_gemini())
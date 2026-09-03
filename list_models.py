from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

print("Modelos disponíveis:")
for model in client.models.list():
    print(f"- {model.name} (suporta generateContent: {model.supported_actions if hasattr(model, 'supported_actions') else 'N/A'})")
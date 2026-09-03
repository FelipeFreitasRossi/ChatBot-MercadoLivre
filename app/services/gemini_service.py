from google import genai
from app.core.config import settings
from app.services.ai_service import AIService
import logging

logger = logging.getLogger(__name__)

class GeminiService(AIService):
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = "gemini-2.0-flash"  # Modelo rápido e gratuito

    async def generate_response(self, messages: list[dict[str, str]]) -> str:
        try:
            # Converte o histórico para o formato da nova API
            # A nova API espera uma lista de Content com role e parts
            history = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                history.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })

            # Se não houver histórico, cria um vazio
            if not history:
                history = [{"role": "user", "parts": [{"text": "Olá"}]}]

            # Inicia chat
            chat = self.client.chats.create(model=self.model, history=history)

            # Envia a última mensagem do usuário
            last_user_msg = next((m for m in reversed(messages) if m["role"] == "user"), None)
            if last_user_msg:
                response = chat.send_message(last_user_msg["content"])
            else:
                response = chat.send_message("Olá")

            return response.text

        except Exception as e:
            logger.error(f"Erro no Gemini: {e}")
            return "Desculpe, estou com dificuldades técnicas. Tente novamente mais tarde."
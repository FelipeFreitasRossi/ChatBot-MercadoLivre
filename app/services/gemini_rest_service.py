import httpx
import logging
from app.core.config import settings
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)

class GeminiRESTService(AIService):
    def __init__(self):
        self.api_key = settings.gemini_api_key
        # Lista de modelos para fallback
        self.models = [
            "gemini-2.5-flash",
            "gemini-3.1-flash-lite",
            "gemini-3.5-flash",
            "gemini-1.5-pro",
        ]

    async def generate_response(self, messages: list[dict[str, str]]) -> str:
        for model in self.models:
            try:
                response = await self._call_gemini(model, messages)
                if response:
                    return response
            except Exception as e:
                logger.warning(f"Falha com modelo {model}: {e}")
                continue
        return "Desculpe, estou com dificuldades técnicas. Tente novamente mais tarde."

    async def _call_gemini(self, model: str, messages: list[dict[str, str]]) -> str | None:
        # System prompt adaptado para a SantoPresentesc
        system_prompt = (
            "Você é um assistente virtual da loja SantoPresentesc. "
            "Sua missão é ajudar clientes a encontrarem a camisa perfeita. "
            "A loja vende três tipos de camisas:\n"
            "- Camisas Oversized (modelo largo e despojado)\n"
            "- Camisas com Estampa (estampas exclusivas)\n"
            "- Babylooks (modelo mais justo e moderno)\n"
            "Siga estas regras:\n"
            "1. Se o cliente não mencionar o que procura, pergunte: 'O que você está procurando hoje? Temos Oversized, estampadas e babylooks.'\n"
            "2. Quando o cliente mencionar um tipo, apresente as opções disponíveis com preço e estoque.\n"
            "3. Pergunte sobre o tamanho e cor preferidos.\n"
            "4. Se o cliente quiser comprar, direcione para o checkout.\n"
            "5. Seja descontraído, amigável e incentive a compra. "
            "Use apenas os dados fornecidos no contexto. Não invente informações."
        )

        contents = [
            {"role": "user", "parts": [{"text": system_prompt}]}
        ]

        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

        if len(contents) == 1:
            contents.append({"role": "user", "parts": [{"text": "Olá"}]})

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 800
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                return candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "Sem resposta")
            return None
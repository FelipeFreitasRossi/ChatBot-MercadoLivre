from abc import ABC, abstractmethod
from typing import List, Dict

class AIService(ABC):
    @abstractmethod
    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Gera uma resposta baseada no histórico de mensagens."""
        pass
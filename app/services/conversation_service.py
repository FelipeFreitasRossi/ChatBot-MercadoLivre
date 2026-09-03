import logging
from sqlalchemy.orm import Session
from app.models import Customer, Conversation, Message
from app.services.ai_service import AIService
from app.services.product_service import ProductService
from app.core.config import settings

logger = logging.getLogger(__name__)

class ConversationService:
    def __init__(self, db: Session, ai_service: AIService):
        self.db = db
        self.ai_service = ai_service

    async def process_message(self, channel: str, external_id: str, content: str) -> str:
        # 1. Obter ou criar cliente
        customer = self.db.query(Customer).filter_by(
            channel=channel, external_id=external_id
        ).first()
        if not customer:
            customer = Customer(channel=channel, external_id=external_id)
            self.db.add(customer)
            self.db.commit()
            self.db.refresh(customer)

        # 2. Obter conversa ativa ou criar nova
        conversation = self.db.query(Conversation).filter_by(
            customer_id=customer.id,
            status="active"
        ).first()
        if not conversation:
            conversation = Conversation(
                customer_id=customer.id,
                channel=channel,
                status="active",
                stage="greeting",
                greeting_sent=False
            )
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)

        # 3. Salvar mensagem recebida
        incoming_msg = Message(
            conversation_id=conversation.id,
            direction="incoming",
            content=content
        )
        self.db.add(incoming_msg)
        self.db.commit()

        # 4. Se a conversa estiver em handoff, não responde
        if conversation.status == "handoff":
            return "Sua conversa foi transferida para um atendente. Aguarde."

        # 5. Gerenciar estágios da conversa
        if not conversation.greeting_sent:
            greeting = (
                "Olá! Sou o assistente virtual da SantoPresentesc. "
                "Como você está hoje? Em que posso ajudar?"
            )
            conversation.stage = "asking_need"
            conversation.greeting_sent = True
            self.db.commit()
            self._save_outgoing(conversation.id, greeting)
            return greeting

        if conversation.stage == "asking_need" and not self._mentions_product(content):
            ask_need = "O que você está procurando hoje? Temos Oversized, estampadas e babylooks. Qual você prefere?"
            conversation.stage = "recommending"
            self.db.commit()
            self._save_outgoing(conversation.id, ask_need)
            return ask_need

        if self._mentions_product(content) and conversation.stage in ["asking_need", "recommending"]:
            conversation.stage = "recommending"
            self.db.commit()

        # 6. Montar contexto
        messages = self.db.query(Message).filter_by(
            conversation_id=conversation.id
        ).order_by(Message.created_at.desc()).limit(settings.context_message_limit).all()
        messages.reverse()

        context_messages = []
        for msg in messages:
            role = "user" if msg.direction == "incoming" else "assistant"
            context_messages.append({"role": role, "content": msg.content})

        # 7. Buscar produtos se a mensagem sugerir consulta
        product_keywords = ["preço", "preco", "valor", "quanto custa", "estoque", "disponibilidade", "produto", "sku", "oversized", "estampada", "babylook"]
        if any(k in content.lower() for k in product_keywords):
            results = ProductService.find_product_by_name(self.db, content)
            if results:
                info_lines = []
                for p in results:
                    price_str = f"R${p['price']:.2f}" if p['price'] is not None else "preço não informado"
                    stock_str = f"{p['stock']} unidades" if p['stock'] is not None else "estoque não disponível"
                    info_lines.append(f"Camisa: {p['name']}, Preço: {price_str}, Estoque: {stock_str}")
                product_info = "\n".join(info_lines)
                context_messages.append({
                    "role": "assistant",
                    "content": f"Dados do banco sobre produtos:\n{product_info}"
                })

        # 8. Chamar IA
        try:
            ai_response = await self.ai_service.generate_response(context_messages)
        except Exception as e:
            logger.error(f"Erro ao chamar IA: {e}")
            ai_response = "Desculpe, estou com dificuldades técnicas. Tente novamente mais tarde."

        # 9. Salvar resposta
        self._save_outgoing(conversation.id, ai_response)

        # 10. Atualizar estágio para checkout se o cliente indicar compra
        if any(k in content.lower() for k in ["quero comprar", "comprar", "pedir", "vou levar", "quero"]):
            conversation.stage = "checkout"
            self.db.commit()

        return ai_response

    def _save_outgoing(self, conversation_id: int, content: str) -> None:
        msg = Message(
            conversation_id=conversation_id,
            direction="outgoing",
            content=content
        )
        self.db.add(msg)
        self.db.commit()

    def _mentions_product(self, text: str) -> bool:
        keywords = ["oversized", "estampada", "babylook", "camisa", "camiseta", "modelo", "tamanho", "cor"]
        return any(k in text.lower() for k in keywords)

    def transfer_to_human(self, conversation_id: int) -> None:
        conv = self.db.query(Conversation).filter_by(id=conversation_id).first()
        if conv:
            conv.status = "handoff"
            self.db.commit()
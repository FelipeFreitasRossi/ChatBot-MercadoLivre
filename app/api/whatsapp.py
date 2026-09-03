import logging
from fastapi import APIRouter, Request, HTTPException, Query
from app.core.config import settings
from app.services.conversation_service import ConversationService
from app.services.gemini_rest_service import GeminiRESTService
from app.database.connection import SessionLocal

router = APIRouter(prefix="/webhook", tags=["WhatsApp"])
logger = logging.getLogger(__name__)

@router.get("/whatsapp")
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge")
):
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        logger.info("Webhook verificado com sucesso!")
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Invalid verify token")

@router.post("/whatsapp")
async def receive_whatsapp_message(request: Request):
    try:
        body = await request.json()
        logger.info(f"Webhook recebido: {body}")

        if "entry" in body:
            for entry in body["entry"]:
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    if "messages" in value:
                        for message in value["messages"]:
                            await process_message(message, value)
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Erro no webhook: {e}")
        return {"status": "error"}

async def process_message(message: dict, value: dict):
    from_number = message.get("from")
    text = message.get("text", {}).get("body", "")
    
    logger.info(f"Mensagem de {from_number}: {text}")

    db = SessionLocal()
    try:
        ai_service = GeminiRESTService()
        service = ConversationService(db, ai_service)
        
        response_text = await service.process_message(
            channel="whatsapp",
            external_id=from_number,
            content=text
        )
        
        await send_whatsapp_message(from_number, response_text)
    finally:
        db.close()

async def send_whatsapp_message(to: str, text: str):
    import httpx
    
    url = f"https://graph.facebook.com/v22.0/{settings.whatsapp_phone_number_id}/messages"
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    
    headers = {
        "Authorization": f"Bearer {settings.whatsapp_access_token}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        logger.info(f"Resposta do WhatsApp: {response.status_code} - {response.text}")
        return response.json()
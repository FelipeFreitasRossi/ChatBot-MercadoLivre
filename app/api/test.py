from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.gemini_rest_service import GeminiRESTService
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/test", tags=["Test"])

class MessageRequest(BaseModel):
    channel: str = "whatsapp"
    external_id: str
    content: str

@router.post("/send")
async def send_test_message(request: MessageRequest, db: Session = Depends(get_db)):
    ai_service = GeminiRESTService()
    service = ConversationService(db, ai_service)
    try:
        response = await service.process_message(
            channel=request.channel,
            external_id=request.external_id,
            content=request.content
        )
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import FastAPI
from app.api import test
from app.api import whatsapp

app = FastAPI(
    title="Chatbot SantoPresentesc",
    description="API para atendimento comercial via WhatsApp",
    version="1.0.0"
)

app.include_router(test.router)
app.include_router(whatsapp.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Chatbot SantoPresentesc está rodando!"}
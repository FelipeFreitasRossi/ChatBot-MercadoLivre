from fastapi import FastAPI

app = FastAPI(
    title="Chatbot WhatsApp + Instagram",
    description="API para atendimento comercial via Meta channels",
    version="0.1.0"
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Chatbot is running"}
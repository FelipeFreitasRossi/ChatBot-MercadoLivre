from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Google Gemini
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    
    # OpenAI (mantido para possível fallback, mas opcional)
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4o-mini", env="OPENAI_MODEL")
    
    # Meta WhatsApp
    whatsapp_verify_token: Optional[str] = Field(None, env="WHATSAPP_VERIFY_TOKEN")
    whatsapp_access_token: Optional[str] = Field(None, env="WHATSAPP_ACCESS_TOKEN")
    whatsapp_phone_number_id: Optional[str] = Field(None, env="WHATSAPP_PHONE_NUMBER_ID")
    
    # Meta Instagram
    instagram_verify_token: Optional[str] = Field(None, env="INSTAGRAM_VERIFY_TOKEN")
    instagram_access_token: Optional[str] = Field(None, env="INSTAGRAM_ACCESS_TOKEN")
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    
    # Contexto
    context_message_limit: int = Field(10, env="CONTEXT_MESSAGE_LIMIT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()
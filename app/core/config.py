from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4o-mini", env="OPENAI_MODEL")
    
    whatsapp_verify_token: Optional[str] = Field(None, env="WHATSAPP_VERIFY_TOKEN")
    whatsapp_access_token: Optional[str] = Field(None, env="WHATSAPP_ACCESS_TOKEN")
    whatsapp_phone_number_id: Optional[str] = Field(None, env="WHATSAPP_PHONE_NUMBER_ID")
    
    instagram_verify_token: Optional[str] = Field(None, env="INSTAGRAM_VERIFY_TOKEN")
    instagram_access_token: Optional[str] = Field(None, env="INSTAGRAM_ACCESS_TOKEN")
    
    database_url: str = Field(..., env="DATABASE_URL")
    context_message_limit: int = Field(10, env="CONTEXT_MESSAGE_LIMIT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()
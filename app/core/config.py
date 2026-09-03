from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4o-mini", env="OPENAI_MODEL")
    
    # Meta WhatsApp
    whatsapp_verify_token: str = Field(..., env="WHATSAPP_VERIFY_TOKEN")
    whatsapp_access_token: str = Field(..., env="WHATSAPP_ACCESS_TOKEN")
    whatsapp_phone_number_id: str = Field(..., env="WHATSAPP_PHONE_NUMBER_ID")
    
    # Meta Instagram
    instagram_verify_token: str = Field(..., env="INSTAGRAM_VERIFY_TOKEN")
    instagram_access_token: str = Field(..., env="INSTAGRAM_ACCESS_TOKEN")
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")  # mysql+pymysql://user:pass@host/db
    
    # Context
    context_message_limit: int = Field(10, env="CONTEXT_MESSAGE_LIMIT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()
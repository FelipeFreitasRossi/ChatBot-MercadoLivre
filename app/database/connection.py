from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Se for SQLite, a URL deve ser sqlite:///./chatbot.db
# Se for MySQL, use settings.database_url
# Vamos adaptar: se database_url começar com "sqlite", usamos SQLite, senão MySQL
if settings.database_url.startswith("sqlite"):
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False}  # necessário para SQLite
    )
else:
    engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
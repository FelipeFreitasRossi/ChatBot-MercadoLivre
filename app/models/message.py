from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum, func
from sqlalchemy.orm import relationship
from app.database.connection import Base
import enum

class MessageDirection(enum.Enum):
    incoming = "incoming"
    outgoing = "outgoing"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    direction = Column(Enum(MessageDirection), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(50), default="text")
    metadata = Column(JSON, nullable=True)  # para guardar ids originais da Meta
    created_at = Column(DateTime, server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")
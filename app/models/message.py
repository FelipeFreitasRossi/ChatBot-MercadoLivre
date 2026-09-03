from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    direction = Column(Enum('incoming', 'outgoing', name='msg_direction'), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(50), default='text')
    meta_data = Column(JSON, nullable=True)  # <-- RENOMEADO de 'metadata' para 'meta_data'
    created_at = Column(DateTime, server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")
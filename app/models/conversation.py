from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from app.database.connection import Base
import enum

class ConversationStatus(enum.Enum):
    active = "active"
    handoff = "handoff"
    closed = "closed"

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    channel = Column(String(20), nullable=False)
    started_at = Column(DateTime, server_default=func.now())
    ended_at = Column(DateTime, nullable=True)
    status = Column(Enum(ConversationStatus), default=ConversationStatus.active)
    last_message_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", backref="conversations")
    messages = relationship("Message", back_populates="conversation")
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.database.connection import Base

class HumanHandoff(Base):
    __tablename__ = "human_handoffs"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    requested_by = Column(Enum('customer', 'system', name='handoff_requested_by'), default='customer')
    handled_by = Column(String(255), nullable=True)
    status = Column(Enum('requested', 'accepted', 'resolved', name='handoff_status'), default='requested')
    created_at = Column(DateTime, server_default=func.now())
    resolved_at = Column(DateTime, nullable=True)
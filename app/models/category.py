from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.connection import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    sku = Column(String(100), unique=True, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
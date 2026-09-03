from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base

class Inventory(Base):
    __tablename__ = "inventory"

    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=0)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
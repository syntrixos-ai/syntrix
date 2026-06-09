"""Expense model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.database.base import Base


class Expense(Base):
    """Expense model"""
    
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)  # Total amount in currency
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    business = relationship("Business", back_populates="expenses")
    
    def __repr__(self) -> str:
        return f"<Expense(id={self.id}, item={self.item_name}, amount={self.amount})>"

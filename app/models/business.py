"""Business model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Business(Base):
    """Business model"""
    
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    business_type = Column(String(100), nullable=False)  # e.g., "retail", "service", "food"
    currency = Column(String(3), default="UGX", nullable=False)  # ISO 4217 code
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="businesses")
    sales = relationship("Sale", back_populates="business", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="business", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="business", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Business(id={self.id}, name={self.name})>"

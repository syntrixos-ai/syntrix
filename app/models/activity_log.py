"""Activity log model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class ActivityLog(Base):
    """Activity log model for tracking user interactions"""
    
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    activity_type = Column(String(50), nullable=False)  # e.g., "sale_recorded", "expense_recorded", "summary_requested"
    metadata = Column(String(500))  # Optional JSON metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    business = relationship("Business", back_populates="activity_logs")
    
    def __repr__(self) -> str:
        return f"<ActivityLog(id={self.id}, activity={self.activity_type})>"

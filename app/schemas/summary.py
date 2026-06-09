"""Summary schemas"""

from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class SummaryResponse(BaseModel):
    """Summary response schema"""
    period: str  # "today", "week", "month"
    total_revenue: Decimal
    total_expenses: Decimal
    profit: Decimal
    profit_margin: Optional[Decimal] = None
    transaction_count: int
    message: str  # AI-generated message
    
    class Config:
        json_schema_extra = {
            "example": {
                "period": "today",
                "total_revenue": 650000,
                "total_expenses": 180000,
                "profit": 470000,
                "profit_margin": 72.31,
                "transaction_count": 5,
                "message": "Your business is profitable today 📈",
            }
        }

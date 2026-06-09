"""Transaction extraction schemas"""

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class TransactionExtraction(BaseModel):
    """Transaction extraction schema from AI"""
    transaction_type: str  # "sale" or "expense"
    item_name: str
    quantity: Decimal
    amount: Decimal
    confidence: Optional[float] = None  # 0-1 confidence score
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_type": "sale",
                "item_name": "shoes",
                "quantity": 3,
                "amount": 120000,
                "confidence": 0.95,
            }
        }

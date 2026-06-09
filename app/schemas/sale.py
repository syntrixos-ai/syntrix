"""Sale schemas"""

from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal


class SaleCreate(BaseModel):
    """Sale creation schema"""
    item_name: str
    quantity: Decimal
    amount: Decimal
    
    class Config:
        json_schema_extra = {
            "example": {
                "item_name": "shoes",
                "quantity": 3,
                "amount": 120000,
            }
        }


class SaleResponse(BaseModel):
    """Sale response schema"""
    id: int
    business_id: int
    item_name: str
    quantity: Decimal
    amount: Decimal
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "business_id": 1,
                "item_name": "shoes",
                "quantity": 3,
                "amount": 120000,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00",
            }
        }

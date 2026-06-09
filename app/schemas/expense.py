"""Expense schemas"""

from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal


class ExpenseCreate(BaseModel):
    """Expense creation schema"""
    item_name: str
    quantity: Decimal
    amount: Decimal
    
    class Config:
        json_schema_extra = {
            "example": {
                "item_name": "fuel",
                "quantity": 1,
                "amount": 50000,
            }
        }


class ExpenseResponse(BaseModel):
    """Expense response schema"""
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
                "item_name": "fuel",
                "quantity": 1,
                "amount": 50000,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00",
            }
        }

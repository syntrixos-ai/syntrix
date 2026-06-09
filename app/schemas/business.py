"""Business schemas"""

from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class BusinessCreate(BaseModel):
    """Business creation schema"""
    name: str
    business_type: str
    currency: str = "UGX"
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John's Shoe Store",
                "business_type": "retail",
                "currency": "UGX",
            }
        }


class BusinessResponse(BaseModel):
    """Business response schema"""
    id: int
    name: str
    business_type: str
    currency: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John's Shoe Store",
                "business_type": "retail",
                "currency": "UGX",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00",
            }
        }

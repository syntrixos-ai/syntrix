"""Chat schemas"""

from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """Chat request schema"""
    business_id: int
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "business_id": 1,
                "message": "Sold 3 shoes at 120k",
            }
        }


class ChatResponse(BaseModel):
    """Chat response schema"""
    business_id: int
    user_message: str
    assistant_message: str
    transaction_recorded: bool
    transaction_type: Optional[str] = None  # "sale", "expense", or None
    
    class Config:
        json_schema_extra = {
            "example": {
                "business_id": 1,
                "user_message": "Sold 3 shoes at 120k",
                "assistant_message": "Done 👍\n\nI've recorded the sale of 3 shoes worth UGX 120,000.\n\nShoes seem to be selling well today.",
                "transaction_recorded": True,
                "transaction_type": "sale",
            }
        }

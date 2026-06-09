"""Transaction extraction using Groq AI"""

import json
import logging
from groq import Groq
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.transaction import TransactionExtraction

logger = logging.getLogger(__name__)


class TransactionExtractor:
    """Extract transactions from natural language using Groq API"""
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
    
    async def extract(self, message: str) -> TransactionExtraction:
        """Extract transaction from user message"""
        try:
            prompt = self._build_prompt(message)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a transaction extraction assistant. Extract sales and expense transactions from user messages. Always respond with valid JSON only.",
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200,
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            transaction_data = json.loads(content)
            transaction = TransactionExtraction(**transaction_data)
            
            logger.info(f"Transaction extracted: {transaction.transaction_type}")
            return transaction
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {e}")
            raise ValueError("Failed to parse transaction from message")
        except ValidationError as e:
            logger.error(f"Invalid transaction data: {e}")
            raise ValueError(f"Invalid transaction format: {e}")
        except Exception as e:
            logger.error(f"Transaction extraction failed: {e}")
            raise ValueError(f"Failed to extract transaction: {e}")
    
    def _build_prompt(self, message: str) -> str:
        """Build extraction prompt"""
        return f"""Extract the transaction from this message:

"{message}"

Respond with ONLY a JSON object with these fields:
{{
  "transaction_type": "sale" or "expense",
  "item_name": "name of item/service",
  "quantity": number,
  "amount": number,
  "confidence": 0.0-1.0
}}

If no transaction can be extracted, set confidence to 0.
Always respond with valid JSON only, no other text."""

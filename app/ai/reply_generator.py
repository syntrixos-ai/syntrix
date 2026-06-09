"""Reply generation using Groq AI"""

import logging
from groq import Groq

from app.core.config import settings

logger = logging.getLogger(__name__)


class ReplyGenerator:
    """Generate friendly AI replies using Groq API"""
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
    
    async def generate_transaction_reply(self, transaction_type: str, item_name: str, quantity: float, amount: float, currency: str) -> str:
        """Generate reply for recorded transaction"""
        try:
            prompt = self._build_transaction_prompt(transaction_type, item_name, quantity, amount, currency)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a friendly business assistant. Respond in a conversational, warm tone. Keep responses brief and supportive.",
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300,
            )
            
            reply = response.choices[0].message.content.strip()
            logger.info(f"Reply generated for {transaction_type}")
            return reply
        
        except Exception as e:
            logger.error(f"Reply generation failed: {e}")
            raise ValueError(f"Failed to generate reply: {e}")
    
    async def generate_summary_reply(self, revenue: float, expenses: float, profit: float, currency: str) -> str:
        """Generate reply for business summary"""
        try:
            prompt = self._build_summary_prompt(revenue, expenses, profit, currency)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a supportive business consultant. Give brief, encouraging insights about their business performance.",
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300,
            )
            
            reply = response.choices[0].message.content.strip()
            logger.info("Summary reply generated")
            return reply
        
        except Exception as e:
            logger.error(f"Summary reply generation failed: {e}")
            raise ValueError(f"Failed to generate summary reply: {e}")
    
    def _build_transaction_prompt(self, transaction_type: str, item_name: str, quantity: float, amount: float, currency: str) -> str:
        """Build transaction reply prompt"""
        action = "sold" if transaction_type == "sale" else "purchased"
        return f"""A user just recorded a business transaction:
- Type: {transaction_type}
- Item: {item_name}
- Quantity: {quantity}
- Amount: {currency} {amount:,.0f}

Generate a brief, friendly acknowledgment (1-2 sentences) that shows you understood the transaction.
Include an emoji. Be conversational, not robotic."""
    
    def _build_summary_prompt(self, revenue: float, expenses: float, profit: float, currency: str) -> str:
        """Build summary reply prompt"""
        return f"""A user asked for their business summary:
- Revenue: {currency} {revenue:,.0f}
- Expenses: {currency} {expenses:,.0f}
- Profit: {currency} {profit:,.0f}

Generate a brief, insightful comment (2-3 sentences) about their business performance.
Include relevant emoji. Be encouraging and supportive."""

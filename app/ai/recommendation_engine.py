"""Recommendation generation using Groq AI"""

import logging
from typing import List
from groq import Groq

from app.core.config import settings

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Generate business recommendations using Groq API"""
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
    
    async def generate_recommendations(self, revenue: float, expenses: float, profit: float, currency: str, top_items: List[dict] = None) -> List[str]:
        """Generate business recommendations"""
        try:
            prompt = self._build_prompt(revenue, expenses, profit, currency, top_items)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a business consultant. Provide practical, actionable recommendations for small businesses.",
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500,
            )
            
            content = response.choices[0].message.content.strip()
            recommendations = [line.strip() for line in content.split("\n") if line.strip() and not line.startswith("#")]
            recommendations = [r for r in recommendations if len(r) > 10]  # Filter out short lines
            
            logger.info(f"Generated {len(recommendations)} recommendations")
            return recommendations[:5]  # Return top 5
        
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            return []  # Return empty list on error
    
    def _build_prompt(self, revenue: float, expenses: float, profit: float, currency: str, top_items: List[dict] = None) -> str:
        """Build recommendation prompt"""
        profit_margin = (profit / revenue * 100) if revenue > 0 else 0
        
        items_info = ""
        if top_items:
            items_info = "\nTop selling items: " + ", ".join([f"{item['name']} ({item['sales']} sold)" for item in top_items[:3]])
        
        return f"""Analyze this business performance and provide 3-5 specific, actionable recommendations:
- Revenue: {currency} {revenue:,.0f}
- Expenses: {currency} {expenses:,.0f}
- Profit: {currency} {profit:,.0f}
- Profit Margin: {profit_margin:.1f}%{items_info}

Provide practical recommendations to improve business performance. Each recommendation should be specific and actionable."""

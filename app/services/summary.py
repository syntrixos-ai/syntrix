"""Summary service"""

import logging
from decimal import Decimal
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.sales import SalesService
from app.services.expenses import ExpensesService
from app.repositories.activity_log import ActivityLogRepository
from app.repositories.business import BusinessRepository
from app.schemas.summary import SummaryResponse

logger = logging.getLogger(__name__)


class SummaryService:
    """Business summary service"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.sales_service = SalesService(session)
        self.expenses_service = ExpensesService(session)
        self.activity_repo = ActivityLogRepository(session)
        self.business_repo = BusinessRepository(session)
    
    async def get_summary(self, business_id: int, period: str = "today") -> SummaryResponse:
        """Get business summary for period"""
        # Verify business exists
        business = await self.business_repo.get_by_id(business_id)
        if not business:
            raise ValueError(f"Business {business_id} not found")
        
        # Get revenue and expenses based on period
        if period == "today":
            revenue = await self.sales_service.get_today_revenue(business_id)
            expenses = await self.expenses_service.get_today_expenses(business_id)
        elif period == "week":
            revenue = await self.sales_service.get_week_revenue(business_id)
            expenses = await self.expenses_service.get_week_expenses(business_id)
        elif period == "month":
            revenue = await self.sales_service.get_month_revenue(business_id)
            expenses = await self.expenses_service.get_month_expenses(business_id)
        else:
            raise ValueError(f"Invalid period: {period}")
        
        # Calculate profit
        profit = revenue - expenses
        profit_margin = (profit / revenue * 100) if revenue > 0 else 0
        
        # Get transaction count
        activities = await self.activity_repo.get_by_business(business_id, skip=0, limit=1000)
        transaction_count = len([a for a in activities if a.activity_type in ["sale_recorded", "expense_recorded"]])
        
        # Generate message
        message = self._generate_summary_message(period, profit, profit_margin, revenue, expenses)
        
        # Log activity
        await self.activity_repo.create(
            business_id=business_id,
            activity_type="summary_requested",
            metadata=f"period:{period}",
        )
        
        await self.session.commit()
        
        return SummaryResponse(
            period=period,
            total_revenue=Decimal(str(revenue)),
            total_expenses=Decimal(str(expenses)),
            profit=Decimal(str(profit)),
            profit_margin=Decimal(str(profit_margin)),
            transaction_count=transaction_count,
            message=message,
        )
    
    def _generate_summary_message(self, period: str, profit: float, profit_margin: float, revenue: float, expenses: float) -> str:
        """Generate summary message"""
        if revenue == 0:
            return "No sales recorded yet. Start by recording your first sale!"
        
        if profit > 0:
            if profit_margin > 80:
                return f"Excellent! Your business is highly profitable. Profit margin: {profit_margin:.1f}% 🚀"
            elif profit_margin > 50:
                return f"Great! Your business is profitable. Profit margin: {profit_margin:.1f}% 📈"
            else:
                return f"Your business is profitable. Profit margin: {profit_margin:.1f}% ✅"
        else:
            return f"Your business is running at a loss this {period}. Review your expenses. ⚠️"

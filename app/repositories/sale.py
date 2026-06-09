"""Sale repository"""

from typing import List, Optional
from sqlalchemy import select, func
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sale import Sale
from app.repositories.base import BaseRepository


class SaleRepository(BaseRepository[Sale]):
    """Sale repository implementation"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, Sale)
    
    async def get_by_business(self, business_id: int, skip: int = 0, limit: int = 100) -> List[Sale]:
        """Get all sales for a business"""
        result = await self.session.execute(
            select(Sale)
            .where(Sale.business_id == business_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_total_revenue(self, business_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> float:
        """Get total revenue for a business"""
        query = select(func.sum(Sale.amount)).where(Sale.business_id == business_id)
        
        if start_date:
            query = query.where(Sale.created_at >= start_date)
        if end_date:
            query = query.where(Sale.created_at < end_date)
        
        result = await self.session.execute(query)
        total = result.scalars().first()
        return float(total) if total else 0.0
    
    async def get_today_revenue(self, business_id: int) -> float:
        """Get today's revenue"""
        today = datetime.utcnow().date()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        return await self.get_total_revenue(business_id, start, end)
    
    async def get_week_revenue(self, business_id: int) -> float:
        """Get this week's revenue"""
        today = datetime.utcnow()
        start = today - timedelta(days=today.weekday())
        return await self.get_total_revenue(business_id, start)
    
    async def get_month_revenue(self, business_id: int) -> float:
        """Get this month's revenue"""
        today = datetime.utcnow()
        start = datetime(today.year, today.month, 1)
        return await self.get_total_revenue(business_id, start)

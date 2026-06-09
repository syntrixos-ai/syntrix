"""Sales service"""

import logging
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sale import Sale
from app.repositories.sale import SaleRepository
from app.repositories.business import BusinessRepository
from app.repositories.activity_log import ActivityLogRepository
from app.schemas.sale import SaleCreate, SaleResponse

logger = logging.getLogger(__name__)


class SalesService:
    """Sales service"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.sale_repo = SaleRepository(session)
        self.business_repo = BusinessRepository(session)
        self.activity_repo = ActivityLogRepository(session)
    
    async def record_sale(self, business_id: int, sale_data: SaleCreate) -> Sale:
        """Record a new sale"""
        # Verify business exists
        business = await self.business_repo.get_by_id(business_id)
        if not business:
            raise ValueError(f"Business {business_id} not found")
        
        # Create sale
        sale = await self.sale_repo.create(
            business_id=business_id,
            item_name=sale_data.item_name,
            quantity=sale_data.quantity,
            amount=sale_data.amount,
        )
        
        # Log activity
        await self.activity_repo.create(
            business_id=business_id,
            activity_type="sale_recorded",
            metadata=f"{sale_data.item_name}:{sale_data.amount}",
        )
        
        await self.session.commit()
        logger.info(f"Sale recorded: {sale.id} - {sale.item_name}")
        return sale
    
    async def get_sale(self, business_id: int, sale_id: int) -> Optional[Sale]:
        """Get sale by ID"""
        sale = await self.sale_repo.get_by_id(sale_id)
        if sale and sale.business_id == business_id:
            return sale
        return None
    
    async def get_business_sales(self, business_id: int, skip: int = 0, limit: int = 100) -> List[Sale]:
        """Get all sales for a business"""
        return await self.sale_repo.get_by_business(business_id, skip, limit)
    
    async def update_sale(self, business_id: int, sale_id: int, **updates) -> Optional[Sale]:
        """Update sale"""
        sale = await self.get_sale(business_id, sale_id)
        if not sale:
            return None
        
        updated = await self.sale_repo.update(sale_id, **updates)
        await self.session.commit()
        logger.info(f"Sale updated: {sale_id}")
        return updated
    
    async def delete_sale(self, business_id: int, sale_id: int) -> bool:
        """Delete sale"""
        sale = await self.get_sale(business_id, sale_id)
        if not sale:
            return False
        
        await self.sale_repo.delete(sale_id)
        await self.session.commit()
        logger.info(f"Sale deleted: {sale_id}")
        return True
    
    async def get_total_revenue(self, business_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> float:
        """Get total revenue for period"""
        return await self.sale_repo.get_total_revenue(business_id, start_date, end_date)
    
    async def get_today_revenue(self, business_id: int) -> float:
        """Get today's revenue"""
        return await self.sale_repo.get_today_revenue(business_id)
    
    async def get_week_revenue(self, business_id: int) -> float:
        """Get this week's revenue"""
        return await self.sale_repo.get_week_revenue(business_id)
    
    async def get_month_revenue(self, business_id: int) -> float:
        """Get this month's revenue"""
        return await self.sale_repo.get_month_revenue(business_id)

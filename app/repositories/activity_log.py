"""Activity log repository"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity_log import ActivityLog
from app.repositories.base import BaseRepository


class ActivityLogRepository(BaseRepository[ActivityLog]):
    """Activity log repository implementation"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, ActivityLog)
    
    async def get_by_business(self, business_id: int, skip: int = 0, limit: int = 100) -> List[ActivityLog]:
        """Get all activity logs for a business"""
        result = await self.session.execute(
            select(ActivityLog)
            .where(ActivityLog.business_id == business_id)
            .order_by(ActivityLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

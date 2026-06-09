"""Business repository"""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business
from app.repositories.base import BaseRepository


class BusinessRepository(BaseRepository[Business]):
    """Business repository implementation"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, Business)
    
    async def get_by_owner(self, owner_id: int) -> List[Business]:
        """Get all businesses owned by a user"""
        result = await self.session.execute(
            select(Business).where(Business.owner_id == owner_id)
        )
        return result.scalars().all()
    
    async def get_by_owner_and_id(self, owner_id: int, business_id: int) -> Optional[Business]:
        """Get business by owner and ID (ownership check)"""
        result = await self.session.execute(
            select(Business).where(
                (Business.owner_id == owner_id) & (Business.id == business_id)
            )
        )
        return result.scalars().first()

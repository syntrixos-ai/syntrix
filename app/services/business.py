"""Business service"""

import logging
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business
from app.repositories.business import BusinessRepository
from app.schemas.business import BusinessCreate, BusinessResponse

logger = logging.getLogger(__name__)


class BusinessService:
    """Business service"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.business_repo = BusinessRepository(session)
    
    async def create_business(self, owner_id: int, business_data: BusinessCreate) -> Business:
        """Create a new business"""
        business = await self.business_repo.create(
            owner_id=owner_id,
            name=business_data.name,
            business_type=business_data.business_type,
            currency=business_data.currency,
        )
        
        await self.session.commit()
        logger.info(f"Business created: {business.name} (id={business.id})")
        return business
    
    async def get_business(self, owner_id: int, business_id: int) -> Optional[Business]:
        """Get business by ID (ownership check)"""
        return await self.business_repo.get_by_owner_and_id(owner_id, business_id)
    
    async def get_user_businesses(self, owner_id: int) -> List[Business]:
        """Get all businesses owned by user"""
        return await self.business_repo.get_by_owner(owner_id)
    
    async def update_business(self, owner_id: int, business_id: int, **updates) -> Optional[Business]:
        """Update business"""
        # Verify ownership
        business = await self.get_business(owner_id, business_id)
        if not business:
            return None
        
        updated = await self.business_repo.update(business_id, **updates)
        await self.session.commit()
        logger.info(f"Business updated: {business_id}")
        return updated
    
    async def delete_business(self, owner_id: int, business_id: int) -> bool:
        """Delete business"""
        # Verify ownership
        business = await self.get_business(owner_id, business_id)
        if not business:
            return False
        
        await self.business_repo.delete(business_id)
        await self.session.commit()
        logger.info(f"Business deleted: {business_id}")
        return True

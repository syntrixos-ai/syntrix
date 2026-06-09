"""Summary endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.main import async_session_maker
from app.services.auth import AuthService
from app.services.business import BusinessService
from app.services.summary import SummaryService
from app.schemas.summary import SummaryResponse

router = APIRouter()


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def get_current_user(authorization: Optional[str] = Header(None), session: AsyncSession = Depends(get_db)):
    """Get current user from token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")
    
    token = authorization[7:]
    try:
        auth_service = AuthService(session)
        return await auth_service.get_current_user(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.get("/", response_model=SummaryResponse)
async def get_summary(
    business_id: int,
    period: str = "today",
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get business summary"""
    try:
        # Verify business ownership
        business_service = BusinessService(session)
        business = await business_service.get_business(current_user.id, business_id)
        if not business:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
        
        if period not in ["today", "week", "month"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid period")
        
        summary_service = SummaryService(session)
        return await summary_service.get_summary(business_id, period)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Summary generation failed")

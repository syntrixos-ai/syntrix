"""Business endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.main import async_session_maker
from app.services.auth import AuthService
from app.services.business import BusinessService
from app.schemas.business import BusinessCreate, BusinessResponse

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


@router.post("/", response_model=BusinessResponse)
async def create_business(business_data: BusinessCreate, session: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    """Create a new business"""
    try:
        service = BusinessService(session)
        business = await service.create_business(current_user.id, business_data)
        return business
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create business")


@router.get("/", response_model=list[BusinessResponse])
async def list_businesses(session: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    """List user's businesses"""
    try:
        service = BusinessService(session)
        businesses = await service.get_user_businesses(current_user.id)
        return businesses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list businesses")


@router.get("/{business_id}", response_model=BusinessResponse)
async def get_business(business_id: int, session: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    """Get business details"""
    try:
        service = BusinessService(session)
        business = await service.get_business(current_user.id, business_id)
        if not business:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
        return business
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get business")

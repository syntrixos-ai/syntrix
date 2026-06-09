"""Sales endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.main import async_session_maker
from app.services.auth import AuthService
from app.services.business import BusinessService
from app.services.sales import SalesService
from app.schemas.sale import SaleCreate, SaleResponse

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


@router.post("/", response_model=SaleResponse)
async def record_sale(business_id: int, sale_data: SaleCreate, session: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    """Record a sale"""
    try:
        # Verify business ownership
        business_service = BusinessService(session)
        business = await business_service.get_business(current_user.id, business_id)
        if not business:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
        
        sales_service = SalesService(session)
        sale = await sales_service.record_sale(business_id, sale_data)
        return sale
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to record sale")


@router.get("/", response_model=list[SaleResponse])
async def list_sales(business_id: int, skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    """List sales for business"""
    try:
        # Verify business ownership
        business_service = BusinessService(session)
        business = await business_service.get_business(current_user.id, business_id)
        if not business:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
        
        sales_service = SalesService(session)
        sales = await sales_service.get_business_sales(business_id, skip, limit)
        return sales
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list sales")

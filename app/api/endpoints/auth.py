"""Authentication endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import async_session_maker
from app.services.auth import AuthService
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.core.security import verify_token

router = APIRouter()


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister, session: AsyncSession = Depends(get_db)):
    """Register a new user"""
    try:
        auth_service = AuthService(session)
        user = await auth_service.register(user_data)
        return await auth_service.login(UserLogin(email=user_data.email, password=user_data.password))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_db)):
    """Login user"""
    try:
        auth_service = AuthService(session)
        return await auth_service.login(user_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed")


@router.post("/refresh", response_model=dict)
async def refresh(token_data: dict, session: AsyncSession = Depends(get_db)):
    """Refresh access token"""
    try:
        auth_service = AuthService(session)
        access_token = await auth_service.refresh_access_token(token_data["refresh_token"])
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Token refresh failed")

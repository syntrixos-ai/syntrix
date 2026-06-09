"""Authentication service"""

import logging
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.core.config import settings

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
    
    async def register(self, user_data: UserRegister) -> User:
        """Register a new user"""
        # Check if email already exists
        if await self.user_repo.email_exists(user_data.email):
            raise ValueError(f"Email {user_data.email} already registered")
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create user
        user = await self.user_repo.create(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
        )
        
        await self.session.commit()
        logger.info(f"User registered: {user.email}")
        return user
    
    async def login(self, user_data: UserLogin) -> TokenResponse:
        """Login user and return tokens"""
        # Get user by email
        user = await self.user_repo.get_by_email(user_data.email)
        
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise ValueError("Invalid email or password")
        
        if not user.is_active:
            raise ValueError("User account is disabled")
        
        # Create tokens
        access_token = create_access_token(user.id, user.email)
        refresh_token = create_refresh_token(user.id)
        
        logger.info(f"User logged in: {user.email}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
    
    async def refresh_access_token(self, refresh_token: str) -> str:
        """Generate new access token from refresh token"""
        token_data = verify_token(refresh_token, token_type="refresh")
        
        if not token_data:
            raise ValueError("Invalid or expired refresh token")
        
        user = await self.user_repo.get_by_id(token_data.user_id)
        if not user or not user.is_active:
            raise ValueError("User not found or inactive")
        
        return create_access_token(user.id, user.email)
    
    async def get_current_user(self, token: str) -> User:
        """Get current user from token"""
        token_data = verify_token(token, token_type="access")
        
        if not token_data:
            raise ValueError("Invalid or expired token")
        
        user = await self.user_repo.get_by_id(token_data.user_id)
        if not user or not user.is_active:
            raise ValueError("User not found or inactive")
        
        return user

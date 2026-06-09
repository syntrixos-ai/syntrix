"""Auth service tests"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth import AuthService
from app.schemas.user import UserRegister, UserLogin


@pytest.mark.asyncio
async def test_user_registration(test_db: AsyncSession):
    """Test user registration"""
    auth_service = AuthService(test_db)
    
    user_data = UserRegister(
        email="test@example.com",
        password="TestPassword123",
        full_name="Test User",
    )
    
    user = await auth_service.register(user_data)
    
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.hashed_password != "TestPassword123"  # Should be hashed


@pytest.mark.asyncio
async def test_duplicate_email_registration(test_db: AsyncSession):
    """Test that duplicate email raises error"""
    auth_service = AuthService(test_db)
    
    user_data = UserRegister(
        email="test@example.com",
        password="TestPassword123",
        full_name="Test User",
    )
    
    await auth_service.register(user_data)
    
    with pytest.raises(ValueError):
        await auth_service.register(user_data)


@pytest.mark.asyncio
async def test_user_login(test_db: AsyncSession):
    """Test user login"""
    auth_service = AuthService(test_db)
    
    user_data = UserRegister(
        email="test@example.com",
        password="TestPassword123",
        full_name="Test User",
    )
    
    await auth_service.register(user_data)
    
    login_data = UserLogin(
        email="test@example.com",
        password="TestPassword123",
    )
    
    token_response = await auth_service.login(login_data)
    
    assert token_response.access_token is not None
    assert token_response.refresh_token is not None
    assert token_response.token_type == "bearer"


@pytest.mark.asyncio
async def test_invalid_login(test_db: AsyncSession):
    """Test login with invalid credentials"""
    auth_service = AuthService(test_db)
    
    user_data = UserRegister(
        email="test@example.com",
        password="TestPassword123",
        full_name="Test User",
    )
    
    await auth_service.register(user_data)
    
    login_data = UserLogin(
        email="test@example.com",
        password="WrongPassword",
    )
    
    with pytest.raises(ValueError):
        await auth_service.login(login_data)

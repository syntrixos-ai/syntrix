"""Business service tests"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth import AuthService
from app.services.business import BusinessService
from app.schemas.user import UserRegister
from app.schemas.business import BusinessCreate


@pytest.mark.asyncio
async def test_create_business(test_db: AsyncSession):
    """Test creating a business"""
    # First create a user
    auth_service = AuthService(test_db)
    user_data = UserRegister(
        email="test@example.com",
        password="TestPassword123",
        full_name="Test User",
    )
    user = await auth_service.register(user_data)
    
    # Create business
    business_service = BusinessService(test_db)
    business_data = BusinessCreate(
        name="Test Business",
        business_type="retail",
        currency="UGX",
    )
    
    business = await business_service.create_business(user.id, business_data)
    
    assert business.name == "Test Business"
    assert business.owner_id == user.id
    assert business.currency == "UGX"


@pytest.mark.asyncio
async def test_get_user_businesses(test_db: AsyncSession):
    """Test retrieving user's businesses"""
    # Create user
    auth_service = AuthService(test_db)
    user_data = UserRegister(
        email="test@example.com",
        password="TestPassword123",
        full_name="Test User",
    )
    user = await auth_service.register(user_data)
    
    # Create businesses
    business_service = BusinessService(test_db)
    
    for i in range(3):
        business_data = BusinessCreate(
            name=f"Business {i}",
            business_type="retail",
        )
        await business_service.create_business(user.id, business_data)
    
    # Get user's businesses
    businesses = await business_service.get_user_businesses(user.id)
    
    assert len(businesses) == 3

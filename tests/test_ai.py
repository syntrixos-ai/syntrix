"""Transaction extractor tests"""

import pytest
from app.ai.transaction_extractor import TransactionExtractor


@pytest.mark.asyncio
async def test_extract_sale_transaction():
    """Test extracting a sale transaction"""
    extractor = TransactionExtractor()
    
    message = "Sold 3 shoes at 120000"
    transaction = await extractor.extract(message)
    
    assert transaction.transaction_type == "sale"
    assert transaction.item_name.lower() == "shoes"
    assert transaction.quantity == 3
    assert transaction.amount == 120000


@pytest.mark.asyncio
async def test_extract_expense_transaction():
    """Test extracting an expense transaction"""
    extractor = TransactionExtractor()
    
    message = "Bought fuel for 50000"
    transaction = await extractor.extract(message)
    
    assert transaction.transaction_type == "expense"
    assert transaction.item_name.lower() == "fuel"
    assert transaction.amount == 50000

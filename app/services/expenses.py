"""Expenses service"""

import logging
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.expense import Expense
from app.repositories.expense import ExpenseRepository
from app.repositories.business import BusinessRepository
from app.repositories.activity_log import ActivityLogRepository
from app.schemas.expense import ExpenseCreate, ExpenseResponse

logger = logging.getLogger(__name__)


class ExpensesService:
    """Expenses service"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.expense_repo = ExpenseRepository(session)
        self.business_repo = BusinessRepository(session)
        self.activity_repo = ActivityLogRepository(session)
    
    async def record_expense(self, business_id: int, expense_data: ExpenseCreate) -> Expense:
        """Record a new expense"""
        # Verify business exists
        business = await self.business_repo.get_by_id(business_id)
        if not business:
            raise ValueError(f"Business {business_id} not found")
        
        # Create expense
        expense = await self.expense_repo.create(
            business_id=business_id,
            item_name=expense_data.item_name,
            quantity=expense_data.quantity,
            amount=expense_data.amount,
        )
        
        # Log activity
        await self.activity_repo.create(
            business_id=business_id,
            activity_type="expense_recorded",
            metadata=f"{expense_data.item_name}:{expense_data.amount}",
        )
        
        await self.session.commit()
        logger.info(f"Expense recorded: {expense.id} - {expense.item_name}")
        return expense
    
    async def get_expense(self, business_id: int, expense_id: int) -> Optional[Expense]:
        """Get expense by ID"""
        expense = await self.expense_repo.get_by_id(expense_id)
        if expense and expense.business_id == business_id:
            return expense
        return None
    
    async def get_business_expenses(self, business_id: int, skip: int = 0, limit: int = 100) -> List[Expense]:
        """Get all expenses for a business"""
        return await self.expense_repo.get_by_business(business_id, skip, limit)
    
    async def update_expense(self, business_id: int, expense_id: int, **updates) -> Optional[Expense]:
        """Update expense"""
        expense = await self.get_expense(business_id, expense_id)
        if not expense:
            return None
        
        updated = await self.expense_repo.update(expense_id, **updates)
        await self.session.commit()
        logger.info(f"Expense updated: {expense_id}")
        return updated
    
    async def delete_expense(self, business_id: int, expense_id: int) -> bool:
        """Delete expense"""
        expense = await self.get_expense(business_id, expense_id)
        if not expense:
            return False
        
        await self.expense_repo.delete(expense_id)
        await self.session.commit()
        logger.info(f"Expense deleted: {expense_id}")
        return True
    
    async def get_total_expenses(self, business_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> float:
        """Get total expenses for period"""
        return await self.expense_repo.get_total_expenses(business_id, start_date, end_date)
    
    async def get_today_expenses(self, business_id: int) -> float:
        """Get today's expenses"""
        return await self.expense_repo.get_today_expenses(business_id)
    
    async def get_week_expenses(self, business_id: int) -> float:
        """Get this week's expenses"""
        return await self.expense_repo.get_week_expenses(business_id)
    
    async def get_month_expenses(self, business_id: int) -> float:
        """Get this month's expenses"""
        return await self.expense_repo.get_month_expenses(business_id)

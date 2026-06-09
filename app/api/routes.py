"""API route aggregator"""

from fastapi import APIRouter
from app.api.endpoints import auth, business, sales, expenses, chat, summary, recommendations

router = APIRouter()

# Include all endpoint routers
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(business.router, prefix="/businesses", tags=["Businesses"])
router.include_router(sales.router, prefix="/sales", tags=["Sales"])
router.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
router.include_router(chat.router, prefix="/chat", tags=["Chat"])
router.include_router(summary.router, prefix="/summary", tags=["Summary"])
router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])

__all__ = ["router"]

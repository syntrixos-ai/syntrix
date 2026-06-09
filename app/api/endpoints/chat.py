"""Chat endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.main import async_session_maker
from app.services.auth import AuthService
from app.services.business import BusinessService
from app.services.sales import SalesService
from app.services.expenses import ExpensesService
from app.ai.transaction_extractor import TransactionExtractor
from app.ai.reply_generator import ReplyGenerator
from app.schemas.chat import ChatRequest, ChatResponse

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


@router.post("/", response_model=ChatResponse)
async def chat(chat_request: ChatRequest, session: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    """Process chat message and extract transactions"""
    try:
        # Verify business ownership
        business_service = BusinessService(session)
        business = await business_service.get_business(current_user.id, chat_request.business_id)
        if not business:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
        
        # Extract transaction from message
        extractor = TransactionExtractor()
        transaction = await extractor.extract(chat_request.message)
        
        # Record transaction if confidence is high
        transaction_recorded = False
        transaction_type = None
        
        if transaction.confidence and transaction.confidence > 0.5:
            if transaction.transaction_type == "sale":
                sales_service = SalesService(session)
                await sales_service.record_sale(chat_request.business_id, transaction)
                transaction_recorded = True
                transaction_type = "sale"
            elif transaction.transaction_type == "expense":
                expenses_service = ExpensesService(session)
                await expenses_service.record_expense(chat_request.business_id, transaction)
                transaction_recorded = True
                transaction_type = "expense"
        
        # Generate friendly reply
        reply_generator = ReplyGenerator()
        if transaction_recorded:
            assistant_message = await reply_generator.generate_transaction_reply(
                transaction_type,
                transaction.item_name,
                float(transaction.quantity),
                float(transaction.amount),
                business.currency,
            )
        else:
            # Generic response if no transaction detected
            assistant_message = "I couldn't understand that transaction. Please try saying something like 'Sold 3 shoes at 120k' or 'Bought fuel for 50k'."
        
        return ChatResponse(
            business_id=chat_request.business_id,
            user_message=chat_request.message,
            assistant_message=assistant_message,
            transaction_recorded=transaction_recorded,
            transaction_type=transaction_type,
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Chat processing failed")

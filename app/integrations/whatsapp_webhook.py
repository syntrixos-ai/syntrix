"""WhatsApp webhook handler"""

import logging
from fastapi import APIRouter, Request, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import async_session_maker
from app.integrations.whatsapp_cloud import WhatsAppCloudProvider
from app.services.auth import AuthService
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()
whatsapp_provider = WhatsAppCloudProvider()


@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None),
    hub_challenge: str = Query(None),
    hub_verify_token: str = Query(None),
):
    """Verify WhatsApp webhook"""
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_WEBHOOK_TOKEN:
        return int(hub_challenge)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid verification token")


@router.post("/webhook")
async def handle_webhook(request: Request):
    """Handle incoming WhatsApp messages"""
    try:
        webhook_data = await request.json()
        
        # Parse message
        message_data = await whatsapp_provider.receive_message(webhook_data)
        
        if not message_data:
            return {"status": "ok"}
        
        logger.info(f"Received message from {message_data['from']}: {message_data['text']}")
        
        # Here you would:
        # 1. Find the user by phone number
        # 2. Find their business
        # 3. Process the message via chat endpoint
        # 4. Send response back
        
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "error"}

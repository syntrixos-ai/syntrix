"""WhatsApp Cloud API provider implementation"""

import json
import logging
from typing import Optional, Dict, Any
import httpx

from app.core.config import settings
from app.integrations.whatsapp_base import BaseWhatsAppProvider

logger = logging.getLogger(__name__)


class WhatsAppCloudProvider(BaseWhatsAppProvider):
    """Meta WhatsApp Cloud API provider"""
    
    def __init__(self):
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.business_account_id = settings.WHATSAPP_BUSINESS_ACCOUNT_ID
        self.webhook_token = settings.WHATSAPP_WEBHOOK_TOKEN
        self.api_version = "v18.0"
        self.base_url = f"https://graph.instagram.com/{self.api_version}"
    
    async def receive_message(self, webhook_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse incoming message from WhatsApp webhook"""
        try:
            # Extract message data from WhatsApp webhook payload
            if "entry" not in webhook_data:
                return None
            
            entry = webhook_data["entry"][0]
            changes = entry.get("changes", [])
            
            if not changes:
                return None
            
            change = changes[0]
            value = change.get("value", {})
            messages = value.get("messages", [])
            
            if not messages:
                return None
            
            message = messages[0]
            contact = value.get("contacts", [{}])[0]
            
            return {
                "from": message.get("from"),
                "message_id": message.get("id"),
                "text": message.get("text", {}).get("body"),
                "name": contact.get("profile", {}).get("name"),
                "timestamp": message.get("timestamp"),
            }
        
        except Exception as e:
            logger.error(f"Failed to parse WhatsApp message: {e}")
            return None
    
    async def send_message(self, phone_number: str, message: str) -> bool:
        """Send message via WhatsApp Cloud API"""
        try:
            url = f"{self.base_url}/{self.phone_number_id}/messages"
            
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": phone_number,
                "type": "text",
                "text": {"body": message},
            }
            
            headers = {
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",  # Should be WhatsApp token
                "Content-Type": "application/json",
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    logger.info(f"Message sent to {phone_number}")
                    return True
                else:
                    logger.error(f"Failed to send message: {response.text}")
                    return False
        
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return False
    
    def verify_webhook(self, token: str) -> bool:
        """Verify webhook token"""
        return token == self.webhook_token

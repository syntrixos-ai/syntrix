"""Base WhatsApp provider interface"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseWhatsAppProvider(ABC):
    """Abstract base class for WhatsApp providers"""
    
    @abstractmethod
    async def receive_message(self, webhook_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Receive and parse message from WhatsApp webhook"""
        pass
    
    @abstractmethod
    async def send_message(self, phone_number: str, message: str) -> bool:
        """Send message to user via WhatsApp"""
        pass
    
    @abstractmethod
    def verify_webhook(self, token: str) -> bool:
        """Verify webhook token"""
        pass

"""Scheduler for background jobs"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta

from app.core.config import settings

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone=settings.SCHEDULER_TIMEZONE)


def start_scheduler():
    """Start the APScheduler"""
    if not scheduler.running:
        scheduler.add_job(
            send_reminder_alerts,
            CronTrigger(hour=9, minute=0),  # 9 AM daily
            id="send_reminders",
            name="Send reminder alerts to inactive users",
        )
        scheduler.start()
        logger.info("Scheduler started")


def stop_scheduler():
    """Stop the APScheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")


async def send_reminder_alerts():
    """Send reminder alerts to users with no activity in 24 hours"""
    try:
        logger.info("Running reminder alert job")
        # This would be implemented with database queries
        # For now, it's a placeholder
        logger.info("Reminder alert job completed")
    except Exception as e:
        logger.error(f"Reminder alert job failed: {e}")

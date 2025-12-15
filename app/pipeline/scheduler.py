"""APScheduler setup for daily pipeline execution."""

import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from app.daily_runner import run_daily_pipeline

logger = logging.getLogger(__name__)


def start_scheduler():
    """Start the scheduler to run pipeline daily at 9am."""
    scheduler = BlockingScheduler()
    
    # Schedule pipeline to run daily at 9:00 AM
    scheduler.add_job(
        run_daily_pipeline,
        trigger=CronTrigger(hour=9, minute=0),
        id='daily_pipeline',
        name='Daily AI News Pipeline',
        replace_existing=True
    )
    
    logger.info("Scheduler started. Pipeline will run daily at 9:00 AM.")
    logger.info("Press Ctrl+C to exit.")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
        scheduler.shutdown()


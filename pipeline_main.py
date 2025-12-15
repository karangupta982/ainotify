"""Entry point for the pipeline service."""

import logging
import sys
from dotenv import load_dotenv
from app.daily_runner import run_daily_pipeline

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    """Run the pipeline once."""
    hours = 24
    top_n = 10
    
    # Allow overriding defaults via CLI args
    if len(sys.argv) > 1:
        hours = int(sys.argv[1])
    if len(sys.argv) > 2:
        top_n = int(sys.argv[2])
    
    logger.info("Starting pipeline service...")
    result = run_daily_pipeline(hours=hours, top_n=top_n)
    
    # Exit code signals success/failure to schedulers (cron/Render jobs)
    exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()


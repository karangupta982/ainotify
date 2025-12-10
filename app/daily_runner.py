import logging
from datetime import datetime
from dotenv import load_dotenv

from app.runner import run_scrapers
from app.services.process_anthropic import process_anthropic_markdown
from app.services.process_youtube import process_youtube_transcripts
from app.services.process_digest import process_digests
from app.services.process_email import send_digest_email
from app.database.models import Base
from app.database.connection import engine

# Load environment variables (API keys, DB URL, email creds).
load_dotenv()

# Configure root logger once for the whole pipeline.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def run_daily_pipeline(hours: int = 24, top_n: int = 10) -> dict:
    """
    Orchestrate the full daily flow: scrape sources, enrich content,
    summarize into digests, and send an email to the subscriber.

    Args:
        hours: Lookback window for scraping and selecting recent digests.
        top_n: Number of ranked articles to include in the outgoing email.

    Returns:
        Execution summary with counts and success status.
    """
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("Starting Daily AI News Aggregator Pipeline")
    logger.info("=" * 60)

    results = {
        "start_time": start_time.isoformat(),
        "scraping": {},
        "processing": {},
        "digests": {},
        "email": {},
        "success": False,
    }

    try:
        logger.info("\n[0/5] Ensuring database tables exist...")
        # try:
            # This is a user-defined context manager from the `app.database.connection` module.
            # It manages the database connection.
        #     with engine.connect() as conn:
        #         # This is a built-in function from the `sqlalchemy` package.
        #         # It creates all tables defined in the Base metadata.
        #         Base.metadata.create_all(engine)
        #         logger.info("✓ Database tables verified/created")
        # except Exception as e:
        #     logger.error(f"Failed to create database tables: {e}")
        #     raise

        # logger.info("\n[1/5] Scraping articles from sources...")
        # scraping_results = run_scrapers(hours=hours)
        # results["scraping"] = {
        #     "youtube": len(scraping_results.get("youtube", [])),
        #     "openai": len(scraping_results.get("openai", [])),
        #     "anthropic": len(scraping_results.get("anthropic", [])),
        # }
        # logger.info(
        #     f"✓ Scraped {results['scraping']['youtube']} YouTube videos, "
        #     f"{results['scraping']['openai']} OpenAI articles, "
        #     f"{results['scraping']['anthropic']} Anthropic articles"
        # )

        # logger.info("\n[2/5] Processing Anthropic markdown...")
        # anthropic_result = process_anthropic_markdown()
        # results["processing"]["anthropic"] = anthropic_result
        # logger.info(
        #     f"✓ Processed {anthropic_result['processed']} Anthropic articles "
        #     f"({anthropic_result['failed']} failed)"
        # )

        # logger.info("\n[3/5] Processing YouTube transcripts...")
        # youtube_result = process_youtube_transcripts()
        # results["processing"]["youtube"] = youtube_result
        # logger.info(
        #     f"✓ Processed {youtube_result['processed']} transcripts "
        #     f"({youtube_result['unavailable']} unavailable)"
        # )

        # logger.info("\n[4/5] Creating digests for articles...")
        # digest_result = process_digests()
        # results["digests"] = digest_result
        # logger.info(
        #     f"✓ Created {digest_result['processed']} digests "
        #     f"({digest_result['failed']} failed out of {digest_result['total']} total)"
        # )

        logger.info("\n[5/5] Generating and sending email digest...")
        email_result = send_digest_email(hours=hours, top_n=top_n)
        results["email"] = email_result

        if email_result.get("skipped"):
            logger.info(f"✓ {email_result.get('message', 'No new digests to send')}")
            results["success"] = True
        elif email_result["success"]:
            logger.info(
                f"✓ Email sent successfully with {email_result['articles_count']} articles"
            )
            results["success"] = True
        else:
            logger.error(
                f"✗ Failed to send email: {email_result.get('error', 'Unknown error')}"
            )

    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}", exc_info=True)
        results["error"] = str(e)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    results["end_time"] = end_time.isoformat()
    results["duration_seconds"] = duration

    logger.info("\n" + "=" * 60)
    logger.info("Pipeline Summary")
    logger.info("=" * 60)
    logger.info(f"Duration: {duration:.1f} seconds")
    logger.info(f"Scraped: {results['scraping']}")
    logger.info(f"Processed: {results['processing']}")
    logger.info(f"Digests: {results['digests']}")
    email_status = "Skipped" if results.get("email", {}).get("skipped") else (
        "Sent" if results["success"] else "Failed"
    )
    logger.info(f"Email: {email_status}")
    logger.info("=" * 60)

    return results


if __name__ == "__main__":
    # Ad-hoc local run with defaults.
    result = run_daily_pipeline(hours=24, top_n=10)
    exit(0 if result["success"] else 1)

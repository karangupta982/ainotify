import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

from app.runner import run_scrapers
from app.services.process_anthropic import process_anthropic_markdown
from app.services.process_youtube import process_youtube_transcripts
from app.services.process_digest import process_digests
from app.services.process_email import send_digest_email_for_user, get_user_profile_from_mongo
from app.database.repository import Repository
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
    summarize into digests, and send personalized emails to all active users.

    Args:
        hours: Lookback window for scraping and selecting recent digests.
        top_n: Number of ranked articles to include in the outgoing email.

    Returns:
        Execution summary with counts and success status.
    """
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("Starting Daily AI News Aggregator Pipeline (Multi-User)")
    logger.info("=" * 60)

    results = {
        "start_time": start_time.isoformat(),
        "scraping": {},
        "processing": {},
        "digests": {},
        "emails": {"sent": 0, "failed": 0, "skipped": 0},
        "users_processed": 0,
        "success": False,
    }

    try:
        repo = Repository()
        
        # Step 1: Get all active users with their channels
        logger.info("\n[1/6] Getting active users and unique channels...")
        active_users = repo.get_active_users_with_channels()
        if not active_users:
            logger.info("No active users found. Exiting pipeline.")
            results["success"] = True
            results["emails"]["skipped"] = 1
            return results
        
        # Get unique channel IDs
        unique_channel_ids = list(repo.get_all_unique_channel_ids())
        logger.info(f"Found {len(active_users)} active users with {len(unique_channel_ids)} unique channels")

        # Step 2: Scrape content once for all channels
        logger.info("\n[2/6] Scraping articles from sources...")
        scraping_results = run_scrapers(hours=hours, channel_ids=unique_channel_ids)
        results["scraping"] = {
            "youtube": len(scraping_results.get("youtube", [])),
            "openai": len(scraping_results.get("openai", [])),
            "anthropic": len(scraping_results.get("anthropic", [])),
        }
        logger.info(
            f"✓ Scraped {results['scraping']['youtube']} YouTube videos, "
            f"{results['scraping']['openai']} OpenAI articles, "
            f"{results['scraping']['anthropic']} Anthropic articles"
        )

        # Step 3: Process content (once for all)
        logger.info("\n[3/6] Processing Anthropic markdown...")
        anthropic_result = process_anthropic_markdown()
        results["processing"]["anthropic"] = anthropic_result
        logger.info(
            f"✓ Processed {anthropic_result['processed']} Anthropic articles "
            f"({anthropic_result['failed']} failed)"
        )

        logger.info("\n[4/6] Processing YouTube transcripts...")
        youtube_result = process_youtube_transcripts()
        results["processing"]["youtube"] = youtube_result
        logger.info(
            f"✓ Processed {youtube_result['processed']} transcripts "
            f"({youtube_result['unavailable']} unavailable)"
        )

        logger.info("\n[5/6] Creating digests for articles...")
        digest_result = process_digests()
        results["digests"] = digest_result
        logger.info(
            f"✓ Created {digest_result['processed']} digests "
            f"({digest_result['failed']} failed out of {digest_result['total']} total)"
        )

        # Step 4: Process each user and send personalized emails
        logger.info(f"\n[6/6] Generating and sending personalized emails for {len(active_users)} users...")
        
        def process_user_email(user_data):
            """Process email for a single user."""
            user_id = user_data["user_id"]
            channel_ids = user_data["channel_ids"]
            
            try:
                # Get user profile from MongoDB
                user_profile = get_user_profile_from_mongo(user_id)
                if not user_profile:
                    logger.warning(f"No profile found for user {user_id}, skipping...")
                    return {"success": False, "user_id": user_id, "error": "No profile found"}
                
                # Send email
                email_result = send_digest_email_for_user(
                    user_id=user_id,
                    user_profile=user_profile,
                    channel_ids=channel_ids,
                    hours=hours,
                    top_n=top_n
                )
                return email_result
            except Exception as e:
                logger.error(f"Error processing user {user_id}: {e}", exc_info=True)
                return {"success": False, "user_id": user_id, "error": str(e)}
        
        # Process users in parallel (max 10 concurrent)
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_user = {
                executor.submit(process_user_email, user_data): user_data
                for user_data in active_users
            }
            
            for future in as_completed(future_to_user):
                user_data = future_to_user[future]
                try:
                    email_result = future.result()
                    if email_result.get("success"):
                        results["emails"]["sent"] += 1
                        logger.info(f"✓ Email sent to user {email_result.get('user_id')}")
                    elif email_result.get("skipped"):
                        results["emails"]["skipped"] += 1
                    else:
                        results["emails"]["failed"] += 1
                        logger.error(f"✗ Failed to send email to user {email_result.get('user_id')}: {email_result.get('error')}")
                    results["users_processed"] += 1
                except Exception as e:
                    results["emails"]["failed"] += 1
                    results["users_processed"] += 1
                    logger.error(f"✗ Exception processing user {user_data['user_id']}: {e}")

        results["success"] = results["emails"]["sent"] > 0 or results["emails"]["skipped"] > 0

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
    logger.info(f"Users processed: {results['users_processed']}")
    logger.info(f"Emails sent: {results['emails']['sent']}, failed: {results['emails']['failed']}, skipped: {results['emails']['skipped']}")
    logger.info("=" * 60)

    return results


if __name__ == "__main__":
    # Ad-hoc local run with defaults.
    result = run_daily_pipeline(hours=100, top_n=10)
    exit(0 if result["success"] else 1)

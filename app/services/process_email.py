"""Service that ranks digests, formats them, and sends the daily email."""

import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

from app.agent.email_agent import EmailAgent, RankedArticleDetail, EmailDigestResponse
from app.agent.curator_agent import CuratorAgent
from app.database.repository import Repository
from app.services.email import send_email, digest_to_html
from app.database.mongo import get_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def get_user_email_from_mongo(user_id: str) -> Optional[str]:
    """Get user's signup email from MongoDB users collection."""
    db = get_db()
    try:
        # user_id is the email (as per signup logic)
        user = db["users"].find_one({"_id": user_id})
        if user and "email" in user:
            return user["email"]
        return None
    except Exception as e:
        logger.error(f"Error fetching user email for {user_id}: {e}")
        return None


def get_user_profile_from_mongo(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user profile from MongoDB."""
    from bson import ObjectId
    
    db = get_db()
    try:
        # Try to convert to ObjectId if it's a valid ObjectId string
        try:
            obj_id = ObjectId(user_id)
        except:
            obj_id = user_id
        
        doc = db["profiles"].find_one({"_id": obj_id})
        if not doc or "profile" not in doc:
            return None
        return doc["profile"]
    except Exception as e:
        logger.error(f"Error fetching profile for user {user_id}: {e}")
        return None


def generate_email_digest_for_user(
    user_id: str,
    user_profile: Dict[str, Any],
    channel_ids: list,
    hours: int = 24,
    top_n: int = 10
) -> EmailDigestResponse:
    """Produce the ranked digest payload for a specific user."""
    curator = CuratorAgent(user_profile)
    email_agent = EmailAgent(user_profile)
    repo = Repository()

    # Get user-specific digests (filtered by channels)
    digests = repo.get_recent_digests_for_user(user_id, channel_ids, hours=hours)
    total = len(digests)

    if total == 0:
        raise ValueError("No digests available for user")

    logger.info(f"Ranking {total} digests for user {user_id}")
    ranked_articles = curator.rank_digests(digests)

    if not ranked_articles:
        logger.error("Failed to rank digests")
        raise ValueError("Failed to rank articles")

    logger.info(f"Generating email digest with top {top_n} articles for user {user_id}")

    article_details = [
        RankedArticleDetail(
            digest_id=a.digest_id,
            rank=a.rank,
            relevance_score=a.relevance_score,
            reasoning=a.reasoning,
            title=next((d["title"] for d in digests if d["id"] == a.digest_id), ""),
            summary=next((d["summary"] for d in digests if d["id"] == a.digest_id), ""),
            url=next((d["url"] for d in digests if d["id"] == a.digest_id), ""),
            article_type=next(
                (d["article_type"] for d in digests if d["id"] == a.digest_id), ""
            ),
        )
        for a in ranked_articles
    ]

    email_digest = email_agent.create_email_digest_response(
        ranked_articles=article_details, total_ranked=len(ranked_articles), limit=top_n
    )

    logger.info(f"Email digest generated successfully for user {user_id}")
    return email_digest


def send_digest_email_for_user(
    user_id: str,
    user_profile: Dict[str, Any],
    channel_ids: list,
    hours: int = 24,
    top_n: int = 10
) -> dict:
    """
    Fetch digests for user, rank them, render email, and send it.
    
    Email recipient priority:
    1. email_to from profile (if user wants to receive at different email)
    2. Signup email (default - from users collection)
    
    MY_EMAIL from .env is used as the sender (SMTP credentials).
    """
    repo = Repository()
    
    # Get recipient email: prefer email_to from profile, fallback to signup email
    recipient_email = None
    
    # First, try email_to from profile (optional - for forwarding to different email)
    if user_profile and user_profile.get("email_to"):
        recipient_email = user_profile.get("email_to")
        logger.info(f"Using email_to from profile: {recipient_email}")
    
    # If no email_to, use signup email (default)
    if not recipient_email:
        recipient_email = get_user_email_from_mongo(user_id)
        if recipient_email:
            logger.info(f"Using signup email: {recipient_email}")
    
    if not recipient_email:
        return {
            "success": False,
            "error": "User email not found. User must have signed up with an email address.",
            "user_id": user_id,
        }

    try:
        result = generate_email_digest_for_user(
            user_id, user_profile, channel_ids, hours=hours, top_n=top_n
        )
        markdown_content = result.to_markdown()
        html_content = digest_to_html(result)

        subject = f"Daily AI News Digest - {result.introduction.greeting.split('for ')[-1] if 'for ' in result.introduction.greeting else 'Today'}"

        send_email(
            subject=subject,
            body_text=markdown_content,
            body_html=html_content,
            recipients=[recipient_email]
        )

        digest_ids = [article.digest_id for article in result.articles]
        marked_count = repo.mark_digests_as_sent_for_user(user_id, digest_ids)

        logger.info(f"Email sent successfully to {recipient_email}! Marked {marked_count} digests as sent for user {user_id}.")
        return {
            "success": True,
            "subject": subject,
            "articles_count": len(result.articles),
            "marked_as_sent": marked_count,
            "user_id": user_id,
            "email": recipient_email,
        }
    except ValueError as e:
        logger.error(f"Error sending email for user {user_id}: {e}")
        return {"success": False, "error": str(e), "user_id": user_id}
    except Exception as e:
        logger.error(f"Unexpected error sending email for user {user_id}: {e}", exc_info=True)
        return {"success": False, "error": str(e), "user_id": user_id}


# Legacy function for backward compatibility (single user)
def send_digest_email(hours: int = 24, top_n: int = 10) -> dict:
    """Legacy function - kept for backward compatibility."""
    logger.warning("Using legacy send_digest_email function. Use send_digest_email_for_user instead.")
    repo = Repository()
    digests = repo.get_recent_digests(hours=hours)

    if len(digests) == 0:
        logger.info("No new digests to send. Nothing to send.")
        return {
            "success": True,
            "skipped": True,
            "message": "No new digests available",
            "articles_count": 0,
        }

    # This won't work without USER_PROFILE, but keeping for compatibility
    return {"success": False, "error": "Legacy function not supported. Use multi-user pipeline."}


if __name__ == "__main__":
    result = send_digest_email(hours=24, top_n=10)
    if result["success"]:
        print("\n=== Email Digest Sent ===")
        print(f"Subject: {result['subject']}")
        print(f"Articles: {result['articles_count']}")
    else:
        print(f"Error: {result['error']}")

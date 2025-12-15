"""Lightweight data access layer over SQLAlchemy models."""

from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any, Set
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from .models import (
    YouTubeVideo, OpenAIArticle, AnthropicArticle, Digest,
    UserChannel, UserSubscription, DigestSend, SubscriptionStatus
)
from .connection import get_session


class Repository:
    """CRUD helpers used by scrapers, processors, and email services."""

    def __init__(self, session: Optional[Session] = None):
        self.session = session or get_session()

    def _bulk_create_items(
        self,
        items: List[dict],
        model_class,
        id_field: str,
        id_attr: str,
    ) -> int:
        """Insert multiple rows if they do not already exist."""
        new_items = []
        for item in items:
            existing = (
                self.session.query(model_class)
                .filter_by(**{id_attr: item[id_field]})
                .first()
            )
            if not existing:
                new_items.append(model_class(**item))
        if new_items:
            self.session.add_all(new_items)
            self.session.commit()
        return len(new_items)

    def create_youtube_video(
        self,
        video_id: str,
        title: str,
        url: str,
        channel_id: str,
        published_at: datetime,
        description: str = "",
        transcript: Optional[str] = None,
    ) -> Optional[YouTubeVideo]:
        existing = self.session.query(YouTubeVideo).filter_by(video_id=video_id).first()
        if existing:
            return None
        video = YouTubeVideo(
            video_id=video_id,
            title=title,
            url=url,
            channel_id=channel_id,
            published_at=published_at,
            description=description,
            transcript=transcript,
        )
        self.session.add(video)
        self.session.commit()
        return video

    def create_openai_article(
        self,
        guid: str,
        title: str,
        url: str,
        published_at: datetime,
        description: str = "",
        category: Optional[str] = None,
    ) -> Optional[OpenAIArticle]:
        existing = self.session.query(OpenAIArticle).filter_by(guid=guid).first()
        if existing:
            return None
        article = OpenAIArticle(
            guid=guid,
            title=title,
            url=url,
            published_at=published_at,
            description=description,
            category=category,
        )
        self.session.add(article)
        self.session.commit()
        return article

    def create_anthropic_article(
        self,
        guid: str,
        title: str,
        url: str,
        published_at: datetime,
        description: str = "",
        category: Optional[str] = None,
    ) -> Optional[AnthropicArticle]:
        existing = self.session.query(AnthropicArticle).filter_by(guid=guid).first()
        if existing:
            return None
        article = AnthropicArticle(
            guid=guid,
            title=title,
            url=url,
            published_at=published_at,
            description=description,
            category=category,
        )
        self.session.add(article)
        self.session.commit()
        return article

    def bulk_create_youtube_videos(self, videos: List[dict]) -> int:
        formatted_videos = [
            {
                "video_id": v["video_id"],
                "title": v["title"],
                "url": v["url"],
                "channel_id": v.get("channel_id", ""),
                "published_at": v["published_at"],
                "description": v.get("description", ""),
                "transcript": v.get("transcript"),
            }
            for v in videos
        ]
        return self._bulk_create_items(
            formatted_videos, YouTubeVideo, "video_id", "video_id"
        )

    def bulk_create_openai_articles(self, articles: List[dict]) -> int:
        formatted_articles = [
            {
                "guid": a["guid"],
                "title": a["title"],
                "url": a["url"],
                "published_at": a["published_at"],
                "description": a.get("description", ""),
                "category": a.get("category"),
            }
            for a in articles
        ]
        return self._bulk_create_items(
            formatted_articles, OpenAIArticle, "guid", "guid"
        )

    def bulk_create_anthropic_articles(self, articles: List[dict]) -> int:
        formatted_articles = [
            {
                "guid": a["guid"],
                "title": a["title"],
                "url": a["url"],
                "published_at": a["published_at"],
                "description": a.get("description", ""),
                "category": a.get("category"),
            }
            for a in articles
        ]
        return self._bulk_create_items(
            formatted_articles, AnthropicArticle, "guid", "guid"
        )

    def get_anthropic_articles_without_markdown(
        self, limit: Optional[int] = None
    ) -> List[AnthropicArticle]:
        query = self.session.query(AnthropicArticle).filter(
            AnthropicArticle.markdown.is_(None)
        )
        if limit:
            query = query.limit(limit)
        return query.all()

    def update_anthropic_article_markdown(self, guid: str, markdown: str) -> bool:
        article = self.session.query(AnthropicArticle).filter_by(guid=guid).first()
        if article:
            article.markdown = markdown
            self.session.commit()
            return True
        return False

    def get_youtube_videos_without_transcript(
        self, limit: Optional[int] = None
    ) -> List[YouTubeVideo]:
        query = self.session.query(YouTubeVideo).filter(
            YouTubeVideo.transcript.is_(None)
        )
        if limit:
            query = query.limit(limit)
        return query.all()

    def update_youtube_video_transcript(self, video_id: str, transcript: str) -> bool:
        video = self.session.query(YouTubeVideo).filter_by(video_id=video_id).first()
        if video:
            video.transcript = transcript
            self.session.commit()
            return True
        return False

    def get_articles_without_digest(
        self, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        articles = []
        seen_ids = set()

        digests = self.session.query(Digest).all()
        for d in digests:
            seen_ids.add(f"{d.article_type}:{d.article_id}")

        youtube_videos = (
            self.session.query(YouTubeVideo)
            .filter(
                YouTubeVideo.transcript.isnot(None),
                YouTubeVideo.transcript != "__UNAVAILABLE__",
            )
            .all()
        )
        for video in youtube_videos:
            key = f"youtube:{video.video_id}"
            if key not in seen_ids:
                articles.append(
                    {
                        "type": "youtube",
                        "id": video.video_id,
                        "title": video.title,
                        "url": video.url,
                        "content": video.transcript or video.description or "",
                        "published_at": video.published_at,
                    }
                )

        openai_articles = self.session.query(OpenAIArticle).all()
        for article in openai_articles:
            key = f"openai:{article.guid}"
            if key not in seen_ids:
                articles.append(
                    {
                        "type": "openai",
                        "id": article.guid,
                        "title": article.title,
                        "url": article.url,
                        "content": article.description or "",
                        "published_at": article.published_at,
                    }
                )

        anthropic_articles = (
            self.session.query(AnthropicArticle)
            .filter(AnthropicArticle.markdown.isnot(None))
            .all()
        )
        for article in anthropic_articles:
            key = f"anthropic:{article.guid}"
            if key not in seen_ids:
                articles.append(
                    {
                        "type": "anthropic",
                        "id": article.guid,
                        "title": article.title,
                        "url": article.url,
                        "content": article.markdown or article.description or "",
                        "published_at": article.published_at,
                    }
                )

        if limit:
            articles = articles[:limit]

        return articles

    def create_digest(
        self,
        article_type: str,
        article_id: str,
        url: str,
        title: str,
        summary: str,
        published_at: Optional[datetime] = None,
    ) -> Optional[Digest]:
        digest_id = f"{article_type}:{article_id}"
        existing = self.session.query(Digest).filter_by(id=digest_id).first()
        if existing:
            return None

        if published_at:
            if published_at.tzinfo is None:
                published_at = published_at.replace(tzinfo=timezone.utc)
            created_at = published_at
        else:
            created_at = datetime.now(timezone.utc)

        digest = Digest(
            id=digest_id,
            article_type=article_type,
            article_id=article_id,
            url=url,
            title=title,
            summary=summary,
            created_at=created_at,
        )
        self.session.add(digest)
        self.session.commit()
        return digest

    def get_recent_digests(
        self, hours: int = 24, exclude_sent: bool = True
    ) -> List[Dict[str, Any]]:
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        query = self.session.query(Digest).filter(Digest.created_at >= cutoff_time)

        if exclude_sent:
            query = query.filter(Digest.sent_at.is_(None))

        digests = query.order_by(Digest.created_at.desc()).all()

        return [
            {
                "id": d.id,
                "article_type": d.article_type,
                "article_id": d.article_id,
                "url": d.url,
                "title": d.title,
                "summary": d.summary,
                "created_at": d.created_at,
                "sent_at": d.sent_at,
            }
            for d in digests
        ]

    def mark_digests_as_sent(self, digest_ids: List[str]) -> int:
        sent_time = datetime.now(timezone.utc)
        updated = (
            self.session.query(Digest)
            .filter(Digest.id.in_(digest_ids))
            .update({Digest.sent_at: sent_time}, synchronize_session=False)
        )
        self.session.commit()
        return updated

    # User-Channel Operations
    def upsert_user_channels(self, user_id: str, channel_ids: List[str]) -> int:
        """Add or update user channels. Returns number of channels added."""
        # Remove existing channels for this user
        self.session.query(UserChannel).filter(UserChannel.user_id == user_id).delete()
        
        # Add new channels
        new_channels = [
            UserChannel(user_id=user_id, channel_id=channel_id)
            for channel_id in channel_ids
        ]
        if new_channels:
            self.session.add_all(new_channels)
            self.session.commit()
        return len(new_channels)

    def get_user_channels(self, user_id: str) -> List[str]:
        """Get all channel IDs for a specific user."""
        channels = self.session.query(UserChannel).filter(
            UserChannel.user_id == user_id
        ).all()
        return [c.channel_id for c in channels]

    def get_all_unique_channel_ids(self) -> Set[str]:
        """Get all unique channel IDs from active users."""
        channels = self.session.query(UserChannel.channel_id).distinct().all()
        return {c[0] for c in channels}

    def delete_user_channels(self, user_id: str) -> int:
        """Delete all channels for a user (when subscription expires)."""
        deleted = self.session.query(UserChannel).filter(
            UserChannel.user_id == user_id
        ).delete()
        self.session.commit()
        return deleted

    # Subscription Operations
    def create_user_subscription(
        self,
        user_id: str,
        status: SubscriptionStatus = SubscriptionStatus.TRIAL,
        plan: Optional[str] = None,
        trial_days: int = 2
    ) -> UserSubscription:
        """Create a new subscription entry for a user."""
        now = datetime.now(timezone.utc)
        trial_expires = now + timedelta(days=trial_days)
        
        subscription = UserSubscription(
            user_id=user_id,
            subscription_status=status,
            subscription_plan=plan,
            trial_started_at=now,
            subscription_expires_at=trial_expires if status == SubscriptionStatus.TRIAL else None,
        )
        self.session.add(subscription)
        self.session.commit()
        return subscription

    def get_user_subscription(self, user_id: str) -> Optional[UserSubscription]:
        """Get subscription for a user."""
        return self.session.query(UserSubscription).filter(
            UserSubscription.user_id == user_id
        ).first()

    def update_subscription(
        self,
        user_id: str,
        status: Optional[SubscriptionStatus] = None,
        plan: Optional[str] = None,
        expires_at: Optional[datetime] = None
    ) -> bool:
        """Update subscription status and plan."""
        subscription = self.get_user_subscription(user_id)
        if not subscription:
            return False
        
        if status:
            subscription.subscription_status = status
        if plan is not None:
            subscription.subscription_plan = plan
        if expires_at:
            subscription.subscription_expires_at = expires_at
        if status == SubscriptionStatus.ACTIVE and not subscription.subscription_started_at:
            subscription.subscription_started_at = datetime.now(timezone.utc)
        
        subscription.updated_at = datetime.now(timezone.utc)
        self.session.commit()
        return True

    def get_active_users_with_channels(self) -> List[Dict[str, Any]]:
        """Get all active users with their channel IDs."""
        now = datetime.now(timezone.utc)
        active_subscriptions = self.session.query(UserSubscription).filter(
            or_(
                UserSubscription.subscription_status == SubscriptionStatus.ACTIVE,
                and_(
                    UserSubscription.subscription_status == SubscriptionStatus.TRIAL,
                    UserSubscription.subscription_expires_at > now
                )
            )
        ).all()
        
        result = []
        for sub in active_subscriptions:
            channels = self.get_user_channels(sub.user_id)
            result.append({
                "user_id": sub.user_id,
                "subscription_status": sub.subscription_status.value,
                "subscription_plan": sub.subscription_plan,
                "channel_ids": channels,
            })
        return result

    def check_subscription_status(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Check if user subscription is active."""
        subscription = self.get_user_subscription(user_id)
        if not subscription:
            return None
        
        now = datetime.now(timezone.utc)
        is_active = (
            subscription.subscription_status == SubscriptionStatus.ACTIVE or
            (
                subscription.subscription_status == SubscriptionStatus.TRIAL and
                subscription.subscription_expires_at and
                subscription.subscription_expires_at > now
            )
        )
        
        return {
            "user_id": subscription.user_id,
            "status": subscription.subscription_status.value,
            "plan": subscription.subscription_plan,
            "is_active": is_active,
            "expires_at": subscription.subscription_expires_at.isoformat() if subscription.subscription_expires_at else None,
        }

    # User-specific Digest Operations
    def get_recent_digests_for_user(
        self,
        user_id: str,
        channel_ids: List[str],
        hours: int = 24
    ) -> List[Dict[str, Any]]:
        """Get recent digests for a user, filtering YouTube videos by their channels."""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        # Get all digests that haven't been sent to this user
        sent_digest_ids = {
            ds.digest_id
            for ds in self.session.query(DigestSend.digest_id).filter(
                DigestSend.user_id == user_id
            ).all()
        }
        
        # Get YouTube videos for user's channels
        if channel_ids:
            youtube_videos = self.session.query(YouTubeVideo).filter(
                YouTubeVideo.channel_id.in_(channel_ids)
            ).all()
            youtube_video_ids = {v.video_id for v in youtube_videos}
        else:
            youtube_video_ids = set()
        
        # Get YouTube digests filtered by user's channels
        youtube_digest_ids = {f"youtube:{vid}" for vid in youtube_video_ids}
        youtube_digests = []
        if youtube_digest_ids:
            youtube_digests = self.session.query(Digest).filter(
                and_(
                    Digest.article_type == "youtube",
                    Digest.created_at >= cutoff_time,
                    Digest.id.in_(youtube_digest_ids),
                    ~Digest.id.in_(sent_digest_ids) if sent_digest_ids else True
                )
            ).all()
        
        # Get OpenAI and Anthropic digests (shared for all users)
        other_digests = self.session.query(Digest).filter(
            and_(
                Digest.article_type.in_(["openai", "anthropic"]),
                Digest.created_at >= cutoff_time,
                ~Digest.id.in_(sent_digest_ids) if sent_digest_ids else True
            )
        ).all()
        
        all_digests = list(youtube_digests) + list(other_digests)
        
        return [
            {
                "id": d.id,
                "article_type": d.article_type,
                "article_id": d.article_id,
                "url": d.url,
                "title": d.title,
                "summary": d.summary,
                "created_at": d.created_at,
            }
            for d in all_digests
        ]

    def mark_digests_as_sent_for_user(self, user_id: str, digest_ids: List[str]) -> int:
        """Mark digests as sent for a specific user."""
        sent_time = datetime.now(timezone.utc)
        count = 0
        
        for digest_id in digest_ids:
            # Check if already sent
            existing = self.session.query(DigestSend).filter(
                and_(
                    DigestSend.digest_id == digest_id,
                    DigestSend.user_id == user_id
                )
            ).first()
            
            if not existing:
                digest_send = DigestSend(
                    digest_id=digest_id,
                    user_id=user_id,
                    sent_at=sent_time
                )
                self.session.add(digest_send)
                count += 1
        
        self.session.commit()
        return count

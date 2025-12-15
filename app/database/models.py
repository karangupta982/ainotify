"""ORM models used across scrapers, processors, and email services."""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()


class SubscriptionStatus(enum.Enum):
    """Subscription status enum."""
    TRIAL = "trial"
    ACTIVE = "active"
    EXPIRED = "expired"


class YouTubeVideo(Base):
    """Raw YouTube metadata plus optional transcript."""

    __tablename__ = "youtube_videos"

    video_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    channel_id = Column(String, nullable=False)
    published_at = Column(DateTime, nullable=False)
    description = Column(Text)
    transcript = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class OpenAIArticle(Base):
    """OpenAI blog/news entry metadata."""

    __tablename__ = "openai_articles"

    guid = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    description = Column(Text)
    published_at = Column(DateTime, nullable=False)
    category = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AnthropicArticle(Base):
    """Anthropic blog/research entry with optional markdown body."""

    __tablename__ = "anthropic_articles"

    guid = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    description = Column(Text)
    published_at = Column(DateTime, nullable=False)
    category = Column(String, nullable=True)
    markdown = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Digest(Base):
    """LLM-generated summary for any source article."""

    __tablename__ = "digests"

    id = Column(String, primary_key=True)
    article_type = Column(String, nullable=False)
    article_id = Column(String, nullable=False)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)


class UserChannel(Base):
    """User-channel associations for YouTube channels."""

    __tablename__ = "user_channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    channel_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "channel_id", name="uq_user_channel"),
    )


class UserSubscription(Base):
    """User subscription tracking."""

    __tablename__ = "user_subscriptions"

    user_id = Column(String, primary_key=True)
    subscription_status = Column(SQLEnum(SubscriptionStatus), nullable=False)
    subscription_plan = Column(String, nullable=True)  # 'starter', 'pro', or None
    trial_started_at = Column(DateTime, nullable=False)
    subscription_started_at = Column(DateTime, nullable=True)
    subscription_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DigestSend(Base):
    """Track which digests have been sent to which users."""

    __tablename__ = "digest_sends"

    id = Column(Integer, primary_key=True, autoincrement=True)
    digest_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("digest_id", "user_id", name="uq_digest_user"),
    )

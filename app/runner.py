"""Helper utilities to run all scrapers and persist raw content."""

from typing import List, Callable, Any, Optional
from .config import YOUTUBE_CHANNELS
from .scrapers.youtube import YouTubeScraper, ChannelVideo
from .scrapers.openai import OpenAIScraper
from .scrapers.anthropic import AnthropicScraper
from .database.repository import Repository


def _save_youtube_videos(
    scraper: YouTubeScraper, repo: Repository, hours: int, channel_ids: List[str] = None
) -> List[ChannelVideo]:
    """
    Fetch and persist the latest YouTube videos for specified channels.

    Args:
        scraper (YouTubeScraper): An instance of the YouTubeScraper class. This is a user-defined type.
        repo (Repository): An instance of the Repository class for database operations. This is a user-defined type.
        hours (int): The number of hours to look back for new videos. This is a built-in integer type.
        channel_ids (List[str]): List of YouTube channel IDs to scrape. If None, uses YOUTUBE_CHANNELS from config.

    Returns:
        List[ChannelVideo]: A list of ChannelVideo objects that were saved. This is a user-defined type.
    """
    videos = []
    video_dicts = []
    
    # Use provided channel_ids or fall back to config
    channels_to_scrape = channel_ids if channel_ids else YOUTUBE_CHANNELS
    
    # This loop iterates through the list of YouTube channel IDs.
    for channel_id in channels_to_scrape:
        # This is a user-defined method from the YouTubeScraper class.
        # It fetches the latest videos for a given channel.
        channel_videos = scraper.get_latest_videos(channel_id, hours=hours)
        videos.extend(channel_videos)
        video_dicts.extend(
            [
                {
                    "video_id": v.video_id,
                    "title": v.title,
                    "url": v.url,
                    "channel_id": channel_id,
                    "published_at": v.published_at,
                    "description": v.description,
                    "transcript": v.transcript,
                }
                for v in channel_videos
            ]
        )
    if video_dicts:
        # This is a user-defined method from the Repository class.
        # It bulk saves the YouTube videos to the database.
        repo.bulk_create_youtube_videos(video_dicts)
    return videos


def _save_rss_articles(
    scraper, repo: Repository, hours: int, save_func: Callable
) -> List[Any]:
    """
    Fetch items from an RSS scraper and persist them using a provided saver.

    Args:
        scraper: An instance of an RSS scraper class (e.g., OpenAIScraper, AnthropicScraper). This is a user-defined type.
        repo (Repository): An instance of the Repository class for database operations. This is a user-defined type.
        hours (int): The number of hours to look back for new articles. This is a built-in integer type.
        save_func (Callable): The function to call to save the articles to the database. This is a built-in callable type.

    Returns:
        List[Any]: A list of article objects that were saved.
    """
    # This is a user-defined method from the scraper instance.
    # It fetches the latest articles from the RSS feed.
    articles = scraper.get_articles(hours=hours)
    if articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category,
            }
            for a in articles
        ]
        # This calls the provided save function to save the articles to the database.
        save_func(article_dicts)
    return articles


def run_scrapers(hours: int = 24, channel_ids: Optional[List[str]] = None) -> dict:
    """
    This user-defined function runs all the scrapers.

    Args:
        hours (int, optional): The number of hours to look back for new items. Defaults to 24.
        channel_ids (List[str], optional): List of YouTube channel IDs to scrape. If None, uses config.

    Returns:
        dict: A dictionary where the keys are the names of the scrapers and the values are the lists of items scraped.
    """
    # This creates a new instance of the Repository class.
    repo = Repository()
    results = {}

    # Run YouTube scraper with specified channels
    try:
        youtube_scraper = YouTubeScraper()
        youtube_videos = _save_youtube_videos(youtube_scraper, repo, hours, channel_ids)
        results["youtube"] = youtube_videos
    except Exception as e:
        results["youtube"] = []
        print(f"Error scraping YouTube: {e}")

    # Run OpenAI scraper
    try:
        openai_scraper = OpenAIScraper()
        openai_articles = _save_rss_articles(
            openai_scraper, repo, hours, repo.bulk_create_openai_articles
        )
        results["openai"] = openai_articles
    except Exception as e:
        results["openai"] = []
        print(f"Error scraping OpenAI: {e}")

    # Run Anthropic scraper
    try:
        anthropic_scraper = AnthropicScraper()
        anthropic_articles = _save_rss_articles(
            anthropic_scraper, repo, hours, repo.bulk_create_anthropic_articles
        )
        results["anthropic"] = anthropic_articles
    except Exception as e:
        results["anthropic"] = []
        print(f"Error scraping Anthropic: {e}")

    return results


# This is a built-in check in Python.
# It ensures that the code inside this block is only executed when the script is run directly.
if __name__ == "__main__":
    # This calls the main scraper runner function.
    results = run_scrapers(hours=24)
    # These are built-in print functions to display the results.
    print(f"YouTube videos: {len(results['youtube'])}")
    print(f"OpenAI articles: {len(results['openai'])}")
    print(f"Anthropic articles: {len(results['anthropic'])}")

"""Scraper for Anthropic blog/research RSS feeds."""

from typing import List, Optional
import requests
from html_to_markdown import convert
from .base import BaseScraper, Article


class AnthropicArticle(Article):
    pass


class AnthropicScraper(BaseScraper):
    @property
    def rss_urls(self) -> List[str]:
        return [
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml",
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_research.xml",
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml",
        ]

    def get_articles(self, hours: int = 24) -> List[AnthropicArticle]:
        """Fetch RSS entries and cast to AnthropicArticle."""
        return [
            AnthropicArticle(**article.model_dump())
            for article in super().get_articles(hours)
        ]

    def url_to_markdown(self, url: str) -> Optional[str]:
        """Fetch article HTML and convert it to markdown for downstream summarization."""
        try:
            response = requests.get(
                url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30
            )
            response.raise_for_status()
            html = response.text
            markdown = convert(html)
            return markdown
        except Exception:
            return None


if __name__ == "__main__":
    scraper = AnthropicScraper()
    articles: List[AnthropicArticle] = scraper.get_articles(hours=100)
    markdown: str = scraper.url_to_markdown(articles[1].url)
    print(markdown)

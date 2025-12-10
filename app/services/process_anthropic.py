"""Service that fetches Anthropic article HTML and stores markdown."""

from typing import Optional
from app.scrapers.anthropic import AnthropicScraper
from app.database.repository import Repository
from .base import BaseProcessService


class AnthropicMarkdownProcessor(BaseProcessService):
    def __init__(self):
        super().__init__()
        self.scraper = AnthropicScraper()
        self.repo = Repository()

    def get_items_to_process(self, limit: Optional[int] = None) -> list:
        """Find Anthropic articles missing markdown."""
        return self.repo.get_anthropic_articles_without_markdown(limit=limit)

    def process_item(self, item) -> Optional[str]:
        """Download the article body and convert to markdown."""
        return self.scraper.url_to_markdown(item.url)

    def save_result(self, item, result: str) -> bool:
        """Persist the converted markdown back to the article row."""
        return self.repo.update_anthropic_article_markdown(item.guid, result)


def process_anthropic_markdown(limit: Optional[int] = None) -> dict:
    """Module-level helper used by the daily runner."""
    processor = AnthropicMarkdownProcessor()
    return processor.process(limit=limit)


if __name__ == "__main__":
    result = process_anthropic_markdown()
    print(f"Total articles: {result['total']}")
    print(f"Processed: {result['processed']}")
    print(f"Failed: {result['failed']}")


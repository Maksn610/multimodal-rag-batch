import re
import logging
from datetime import datetime
from typing import Optional
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


def load_issue_page(page: Page, url: str) -> bool:
    page.goto(url, timeout=20000)
    result = "Page Not Found" not in page.title()
    logger.info(f"Loaded page {url}: {'OK' if result else 'NOT FOUND'}")
    return result


def extract_issue_date(page: Page) -> Optional[str]:
    html = page.content()

    match = re.search(r'"datePublished"\s*:\s*"([^"]+)"', html)
    if match:
        try:
            dt = datetime.fromisoformat(match.group(1).replace("Z", "+00:00"))
            return dt.strftime("%B %d, %Y")
        except Exception as e:
            logger.warning(f"Failed to parse JSON-LD date: {e}")

    tag_match = re.search(r'<meta[^>]+property="article:tag"[^>]+content="(.*?)"', html)
    if tag_match and re.search(r'\d{4}', tag_match.group(1)):
        return tag_match.group(1)

    logger.warning("Issue date not found")
    return None

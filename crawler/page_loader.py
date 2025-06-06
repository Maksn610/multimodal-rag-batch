import re
from playwright.sync_api import Page
from typing import Optional
from datetime import datetime


def load_issue_page(page: Page, url: str) -> bool:
    page.goto(url, timeout=20000)
    return "Page Not Found" not in page.title()


def extract_issue_date(page: Page) -> Optional[str]:
    """
    Extracts issue date in human-readable format (e.g. 'January 22, 2025').
    """
    html = page.content()

    # Try JSON-LD
    match = re.search(r'"datePublished"\s*:\s*"([^"]+)"', html)
    if match:
        try:
            # Parse ISO and format
            dt = datetime.fromisoformat(match.group(1).replace("Z", "+00:00"))
            return dt.strftime("%B %d, %Y")  # e.g., January 22, 2025
        except Exception:
            pass

    # Fallback: article:tag
    tag_match = re.search(r'<meta[^>]+property="article:tag"[^>]+content="(.*?)"', html)
    if tag_match and re.search(r'\d{4}', tag_match.group(1)):
        return tag_match.group(1)

    return None

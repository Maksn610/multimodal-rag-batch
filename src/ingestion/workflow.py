import time
import json
import logging
from playwright.sync_api import sync_playwright, TimeoutError
from src.config import START_ISSUE, END_ISSUE, RAW_DIR, IMAGES_DIR
from src.ingestion.page_loader import load_issue_page, extract_issue_date
from src.ingestion.article_parser import extract_articles

logger = logging.getLogger(__name__)


def run_ingestion() -> None:
    RAW_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        for issue_number in range(START_ISSUE, END_ISSUE - 1, -1):
            output_path = RAW_DIR / f"issue_{issue_number}.json"
            if output_path.exists():
                logger.info(f"Issue {issue_number} already exists. Skipping.")
                continue

            url = f"https://www.deeplearning.ai/the-batch/issue-{issue_number}/"
            try:
                logger.info(f"Processing issue {issue_number}...")

                if not load_issue_page(page, url):
                    logger.warning(f"Issue {issue_number} not found.")
                    continue

                issue_title = page.title().strip()
                issue_date = extract_issue_date(page)
                articles = extract_articles(page, issue_number)

                output_data = {
                    "issue_id": f"issue_{issue_number}",
                    "issue_title": issue_title,
                    "issue_url": url,
                    "issue_date": issue_date,
                    "articles": articles
                }

                with output_path.open("w", encoding="utf-8") as f:
                    json.dump(output_data, f, ensure_ascii=False, indent=2)

                logger.info(f"Issue {issue_number} saved to {output_path}")
                time.sleep(1)

            except TimeoutError:
                logger.warning(f"Issue {issue_number} failed to load (timeout).")
            except Exception as e:
                logger.exception(f"Unexpected error with issue {issue_number}: {e}")

        browser.close()

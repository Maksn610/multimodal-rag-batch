import os
import logging
from playwright.sync_api import Page
from src.utils.text_utils import html_to_markdown_text
from src.ingestion.image_downloader import download_and_store_image

logger = logging.getLogger(__name__)
IGNORED_TAGS = {"script", "style", "meta", "link", "head"}


def extract_articles(page: Page, issue_number: int) -> list:
    article_locator = page.locator("article").first
    all_elements = article_locator.locator("*").all()
    articles = []

    current_article = None
    current_section = None
    article_counter = 0
    is_first_h1 = True

    image_subdir = os.path.join("data", "images", f"issue_{issue_number}")
    os.makedirs(image_subdir, exist_ok=True)

    for element in all_elements:
        tag = element.evaluate("el => el.tagName.toLowerCase()")
        if current_article is None and tag not in IGNORED_TAGS:
            current_article = {
                "title": "Introductory Section",
                "text_blocks": [],
                "section_title": None,
                "issue_number": issue_number
            }

        if tag == "h1":
            text = element.inner_text().strip()
            if is_first_h1:
                is_first_h1 = False
                continue
            if text.lower() in ["news", "research", "perspective"]:
                current_section = text
                continue
            if current_article and current_article["text_blocks"]:
                current_article["position"] = article_counter
                current_article["issue_number"] = issue_number
                articles.append(current_article)
                article_counter += 1
            current_article = {
                "title": text,
                "text_blocks": [],
                "section_title": current_section,
                "issue_number": issue_number
            }

        elif tag == "p" and current_article:
            html = element.inner_html()
            if not html.strip():
                continue
            markdown = html_to_markdown_text(html)
            if markdown:
                current_article["text_blocks"].append({
                    "type": "text",
                    "text": markdown
                })

        elif tag == "img" and current_article:
            raw_src = element.get_attribute("src")
            if not raw_src:
                continue
            image_data = download_and_store_image(raw_src, issue_number, image_subdir)
            if image_data is not None:
                current_article["text_blocks"].append({
                    "type": "image",
                    "url": image_data["url"],
                    "local_path": image_data["local_path"]
                })
                alt = element.get_attribute("alt")
                if alt:
                    current_article["text_blocks"].append({
                        "type": "alt_text",
                        "text": alt.strip()
                    })

    if current_article and current_article["text_blocks"]:
        current_article["position"] = article_counter
        current_article["issue_number"] = issue_number
        articles.append(current_article)

    logger.info(f"Extracted {len(articles)} articles from issue {issue_number}")
    return articles

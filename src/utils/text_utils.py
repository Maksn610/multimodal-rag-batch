import re
from bs4 import BeautifulSoup
from src.utils.url_utils import clean_url


def normalize_text(text: str) -> str:
    text = text.replace("’", "'").replace("–", "-").replace("“", '"').replace("”", '"')
    text = text.replace("•", "-").replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def html_to_markdown_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a"):
        href = clean_url(a.get("href", "").strip())
        label = a.get_text(strip=True)
        a.replace_with(f"[{label}]({href})")
    return normalize_text(soup.get_text())

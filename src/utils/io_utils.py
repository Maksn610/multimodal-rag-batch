import json
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def convert_to_jsonl(raw_path: Path, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with raw_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError) as e:
        logger.error(f"Failed to load raw JSON from {raw_path}: {e}")
        return

    if "articles" not in raw or not isinstance(raw["articles"], list):
        logger.error(f"Invalid JSON format: missing 'articles' array")
        return

    try:
        with out_path.open("w", encoding="utf-8") as f:
            for article in raw["articles"]:
                f.write(json.dumps(article, ensure_ascii=False) + "\n")
        logger.info(f"Converted {len(raw['articles'])} articles to JSONL → {out_path}")
    except OSError as e:
        logger.error(f"Failed to write JSONL to {out_path}: {e}")


def load_articles(path: Path) -> List[Dict[str, Any]]:
    articles = []

    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    articles.append(json.loads(line))
                except json.JSONDecodeError as e:
                    logger.warning(f"Skipping invalid JSON line: {e}")
    except (FileNotFoundError, OSError) as e:
        logger.error(f"Failed to open JSONL file {path}: {e}")

    return articles

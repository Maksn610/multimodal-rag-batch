import json
from pathlib import Path
from typing import List, Dict, Any


def convert_to_jsonl(raw_path: Path, out_path: Path) -> None:
    """
    Converts raw JSON to JSONL (one article per line).
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with raw_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError) as e:
        print(f"[ERROR] Failed to load raw JSON from {raw_path}: {e}")
        return

    if "articles" not in raw or not isinstance(raw["articles"], list):
        print(f"[ERROR] Invalid JSON format: missing 'articles' array")
        return

    try:
        with out_path.open("w", encoding="utf-8") as f:
            for article in raw["articles"]:
                f.write(json.dumps(article, ensure_ascii=False) + "\n")
        print(f"[INFO] Converted {len(raw['articles'])} articles to JSONL → {out_path}")
    except OSError as e:
        print(f"[ERROR] Failed to write JSONL to {out_path}: {e}")


def load_articles(path: Path) -> List[Dict[str, Any]]:
    """
    Loads articles from a JSONL file into a list of dicts.
    """
    articles = []

    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    articles.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"[WARNING] Skipping invalid JSON line: {e}")
    except (FileNotFoundError, OSError) as e:
        print(f"[ERROR] Failed to open JSONL file {path}: {e}")

    return articles

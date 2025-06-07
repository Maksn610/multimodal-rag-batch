import json
from pathlib import Path
from typing import List, Dict, Any


def convert_to_jsonl(raw_path: Path, out_path: Path) -> None:
    """
    Converts raw JSON to JSONL (one article per line).
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with raw_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    with out_path.open("w", encoding="utf-8") as f:
        for article in raw["articles"]:
            f.write(json.dumps(article, ensure_ascii=False) + "\n")

    print(f"[INFO] Converted {len(raw['articles'])} articles to JSONL → {out_path}")


def load_articles(path: Path) -> List[Dict[str, Any]]:
    """
    Loads articles from a JSONL file into a list of dicts.
    """
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

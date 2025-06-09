import json
import logging
from tqdm import tqdm
from pathlib import Path

from src.embedding.embedding_client import get_embedding
from src.indexing.index_utils import build_faiss_index, save_index, save_metadata
from src.utils.io_utils import convert_to_jsonl, load_articles
from src.utils.text_formatter import prepare_text
from src.utils.id_utils import generate_article_id
from src.indexing.schema import ArticleMeta
from src.config import (
    RAW_DIR,
    JSONL_DIR,
    INDEX_OUTPUT_PATH,
    METADATA_OUTPUT_PATH,
    EMBED_CACHE_PATH,
    DIM
)

logger = logging.getLogger(__name__)


def run_embedding_pipeline() -> None:
    JSONL_DIR.mkdir(parents=True, exist_ok=True)

    # Load embedding cache
    existing_ids = set()
    if EMBED_CACHE_PATH.exists():
        with EMBED_CACHE_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    existing_ids.add(obj["id"])
                except json.JSONDecodeError:
                    continue

    all_articles = []
    for json_path in sorted(RAW_DIR.glob("issue_*.json")):
        jsonl_path = JSONL_DIR / f"{json_path.stem}.jsonl"
        if not jsonl_path.exists():
            logger.info(f"Converting {json_path} → {jsonl_path}")
            convert_to_jsonl(json_path, jsonl_path)

        logger.info(f"Loading articles from {jsonl_path}")
        issue_id = json_path.stem
        articles = load_articles(jsonl_path)

        for article in articles:
            article["issue_id"] = issue_id
            all_articles.append(article)

    logger.info(f"Total articles to embed: {len(all_articles)}")
    vectors = []
    metadata = []

    for article in tqdm(all_articles):
        article_id = generate_article_id(article["issue_id"], article["title"])
        if article_id in existing_ids:
            logger.info(f"Skipping already embedded article: {article_id}")
            continue

        text = prepare_text(article)
        embedding = get_embedding(text)

        vectors.append(embedding)
        metadata.append(ArticleMeta(
            id=article_id,
            title=article["title"],
            text_snippet=text[:300],
            full_text=text,
            local_image_paths=[
                b["local_path"] for b in article["text_blocks"] if b["type"] == "image"
            ]
        ))

        EMBED_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with EMBED_CACHE_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "id": article_id,
                "title": article["title"]
            }, ensure_ascii=False) + "\n")

    unique_metadata = {}
    for entry in metadata:
        if entry.id not in unique_metadata:
            unique_metadata[entry.id] = entry
    metadata = list(unique_metadata.values())

    if vectors:
        index = build_faiss_index(vectors, dim=DIM)
        save_index(index, INDEX_OUTPUT_PATH)
        save_metadata(metadata, METADATA_OUTPUT_PATH)
        logger.info(f"Index and metadata saved:\n → {INDEX_OUTPUT_PATH}\n → {METADATA_OUTPUT_PATH}")
    else:
        logger.info("No new embeddings were generated — skipping index save.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_embedding_pipeline()

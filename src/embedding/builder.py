import logging
from tqdm import tqdm
from pathlib import Path

from src.embedding.embedding_client import get_embedding
from src.indexing.index_utils import build_faiss_index, save_index, save_metadata
from src.utils.io_utils import convert_to_jsonl, load_articles
from src.indexing.schema import ArticleMeta
from src.config import RAW_DIR, JSONL_DIR, INDEX_OUTPUT_PATH, METADATA_OUTPUT_PATH, DIM

logger = logging.getLogger(__name__)


def prepare_text(article: dict) -> str:
    text_blocks = " ".join([tb["text"] for tb in article["text_blocks"] if tb["type"] == "text"])
    alt_texts = " ".join([tb["text"] for tb in article["text_blocks"] if tb["type"] == "alt_text"])
    return f"{article['title']}\n\n{text_blocks}\n\n{alt_texts}"


def run_embedding_pipeline() -> None:
    JSONL_DIR.mkdir(parents=True, exist_ok=True)

    all_articles = []
    for json_path in sorted(RAW_DIR.glob("issue_*.json")):
        jsonl_path = JSONL_DIR / f"{json_path.stem}.jsonl"
        if not jsonl_path.exists():
            logger.info(f"Converting {json_path} → {jsonl_path}")
            convert_to_jsonl(json_path, jsonl_path)

        logger.info(f"Loading articles from {jsonl_path}")
        all_articles.extend(load_articles(jsonl_path))

    logger.info(f"Total articles to embed: {len(all_articles)}")
    vectors = []
    metadata = []

    for i, article in enumerate(tqdm(all_articles)):
        text = prepare_text(article)
        embedding = get_embedding(text)

        vectors.append(embedding)
        metadata.append(ArticleMeta(
            id=i,
            title=article["title"],
            text_snippet=text[:300],
            local_image_paths=[
                b["local_path"] for b in article["text_blocks"] if b["type"] == "image"
            ]
        ))

    index = build_faiss_index(vectors, dim=DIM)
    save_index(index, INDEX_OUTPUT_PATH)
    save_metadata(metadata, METADATA_OUTPUT_PATH)

    logger.info(f"Index and metadata saved:\n → {INDEX_OUTPUT_PATH}\n → {METADATA_OUTPUT_PATH}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_embedding_pipeline()

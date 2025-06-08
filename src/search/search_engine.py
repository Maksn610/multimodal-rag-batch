import json
import logging
import numpy as np
import faiss
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from src.embedding.embedding_client import get_embedding
from src.indexing.schema import ArticleMeta
from src.config import INDEX_OUTPUT_PATH, METADATA_OUTPUT_PATH, TOP_K, SCORE_THRESHOLD

logger = logging.getLogger(__name__)


def load_index(index_path: Path) -> faiss.Index:
    logger.info(f"Loading FAISS index from {index_path}")
    return faiss.read_index(str(index_path))


def load_metadata(metadata_path: Path) -> List[Union[Dict[str, Any], ArticleMeta]]:
    logger.info(f"Loading metadata from {metadata_path}")
    with metadata_path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def search(
        query: str,
        index: faiss.Index,
        metadata: List[Union[Dict[str, Any], ArticleMeta]],
        top_k: int = TOP_K,
        score_threshold: Optional[float] = SCORE_THRESHOLD
) -> List[Dict[str, Any]]:
    query_embedding = get_embedding(query)
    distances, indices = index.search(np.array([query_embedding]), top_k)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if score_threshold is not None and dist > score_threshold:
            continue
        result = metadata[idx].copy()
        result["score"] = float(dist)
        results.append(result)

    logger.info(f"Found {len(results)} relevant results for query: '{query}'")
    return results


def pretty_print_results(results: List[Dict[str, Any]]) -> None:
    print("\n🔗 Top Relevant Articles:\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. 📰 {result['title']}  (Score: {result['score']:.4f})")
        print(f"   🧾 Snippet: {result['text_snippet'][:200].strip()}...\n")
        if result["local_image_paths"]:
            for path in result["local_image_paths"]:
                print(f"   🖼️ Image: {path}")
        print("-" * 80)


def search_to_json(query: str, top_k: int = TOP_K, score_threshold: Optional[float] = SCORE_THRESHOLD) -> List[
    Dict[str, Any]]:
    index = load_index(INDEX_OUTPUT_PATH)
    metadata = load_metadata(METADATA_OUTPUT_PATH)
    return search(query, index, metadata, top_k, score_threshold)


def run_search():
    import logging
    logging.basicConfig(level=logging.INFO)

    query = input("🔍 Enter your search query: ")
    index = load_index(INDEX_OUTPUT_PATH)
    metadata = load_metadata(METADATA_OUTPUT_PATH)
    results = search(query, index, metadata, top_k=TOP_K, score_threshold=SCORE_THRESHOLD)
    pretty_print_results(results)


if __name__ == "__main__":
    run_search()

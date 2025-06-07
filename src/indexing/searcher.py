import json
import numpy as np
import faiss
from pathlib import Path
from typing import List, Dict, Any
from indexing.embedding.embedding_client import get_embedding

INDEX_PATH = Path("storage/faiss/index_flat_L2.index")
METADATA_PATH = Path("storage/faiss/metadata.jsonl")
TOP_K = 3

def load_index(index_path: Path) -> faiss.Index:
    return faiss.read_index(str(index_path))


def load_metadata(metadata_path: Path) -> List[Dict[str, Any]]:
    with metadata_path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def search(query: str, index: faiss.Index, metadata: List[Dict[str, Any]], top_k: int = TOP_K) -> List[Dict[str, Any]]:
    query_embedding = get_embedding(query)
    distances, indices = index.search(np.array([query_embedding]), top_k)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        result = metadata[idx].copy()
        result["score"] = float(dist)
        results.append(result)

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


def search_to_json(query: str, top_k: int = TOP_K) -> List[Dict[str, Any]]:
    index = load_index(INDEX_PATH)
    metadata = load_metadata(METADATA_PATH)
    return search(query, index, metadata, top_k)


def run_search():
    query = input("🔍 Enter your search query: ")
    index = load_index(INDEX_PATH)
    metadata = load_metadata(METADATA_PATH)
    results = search(query, index, metadata)
    pretty_print_results(results)


if __name__ == "__main__":
    run_search()

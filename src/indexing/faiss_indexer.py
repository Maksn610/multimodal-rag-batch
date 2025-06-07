import json
from pathlib import Path
from tqdm import tqdm
from indexing.embedding.embedding_client import get_embedding
from indexing.vector_db.index_utils import build_faiss_index,save_index,save_metadata

# === CONFIG ===
RAW_JSON_PATH = Path("../../data/issue_290.json")
JSONL_PATH = Path("data/parsed_issues/issue_290.jsonl")
INDEX_OUTPUT_PATH = Path("storage/faiss/index_flat_L2.index")
METADATA_OUTPUT_PATH = Path("storage/faiss/metadata.jsonl")
DIM = 1536
TOP_K = 3


def convert_to_jsonl(raw_path: Path, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with raw_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    with out_path.open("w", encoding="utf-8") as f:
        for article in raw["articles"]:
            f.write(json.dumps(article, ensure_ascii=False) + "\n")
    print(f"[INFO] Converted {len(raw['articles'])} articles to JSONL → {out_path}")


def load_articles(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def prepare_text(article) -> str:
    text_blocks = " ".join([tb["text"] for tb in article["text_blocks"] if tb["type"] == "text"])
    alt_texts = " ".join([tb["text"] for tb in article["text_blocks"] if tb["type"] == "alt_text"])
    return f"{article['title']}\n\n{text_blocks}\n\n{alt_texts}"


def run_indexing():
    if not JSONL_PATH.exists():
        print("[INFO] JSONL not found. Converting from raw JSON...")
        convert_to_jsonl(RAW_JSON_PATH, JSONL_PATH)

    articles = load_articles(JSONL_PATH)
    vectors = []
    metadata = []

    print(f"[INFO] Processing {len(articles)} articles...")

    for i, article in enumerate(tqdm(articles)):
        text = prepare_text(article)
        embedding = get_embedding(text)

        vectors.append(embedding)
        metadata.append({
            "id": i,
            "title": article["title"],
            "text_snippet": text[:300],
            "local_image_paths": [b["local_path"] for b in article["text_blocks"] if b["type"] == "image"]
        })

    index = build_faiss_index(vectors, dim=DIM)
    save_index(index, INDEX_OUTPUT_PATH)
    save_metadata(metadata, METADATA_OUTPUT_PATH)

    print(f"[SUCCESS] Index and metadata saved:\n → {INDEX_OUTPUT_PATH}\n → {METADATA_OUTPUT_PATH}")


if __name__ == "__main__":
    run_indexing()

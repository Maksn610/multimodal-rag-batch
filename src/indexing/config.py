from pathlib import Path

RAW_JSON_PATH = Path("../../data/issue_290.json")
JSONL_PATH = Path("data/parsed_issues/issue_290.jsonl")
INDEX_OUTPUT_PATH = Path("src/indexing/storage/faiss/index_flat_L2.index")
METADATA_OUTPUT_PATH = Path("src/indexing/storage/faiss/metadata.jsonl")


DIM = 1536
TOP_K = 3

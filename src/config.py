import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# =======================
# ⚙️ Ingestion settings
# =======================
START_ISSUE = 290
END_ISSUE = 285

# =======================
# 🔐 Embedding config
# =======================
EMBED_MODEL = "text-embedding-3-small"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# =======================
# 📂 Data paths
# =======================
RAW_DIR = Path("data")
IMAGES_DIR = RAW_DIR / "images"
JSONL_DIR = RAW_DIR / "jsonl"

# =======================
# 📐 FAISS index config
# =======================
DIM = 1536
TOP_K = 3
SCORE_THRESHOLD = None

# Index settings
INDEX_NAME = "index_flat_L2.index"  # You can change to: index_ivf_L2.index, index_hnsw_L2.index, etc.
INDEX_OUTPUT_PATH = Path("storage/faiss") / INDEX_NAME
METADATA_OUTPUT_PATH = Path("storage/faiss/metadata.jsonl")

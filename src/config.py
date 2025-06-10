import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# =======================
# 📌 Base path
# =======================
PROJECT_ROOT = Path(__file__).resolve().parent.parent

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
EMBED_CACHE_PATH = PROJECT_ROOT / "storage/faiss/embedding_cache.jsonl"

# =======================
# 📂 Data paths
# =======================
RAW_DIR = PROJECT_ROOT / "data"
IMAGES_DIR = RAW_DIR / "images"
JSONL_DIR = RAW_DIR / "jsonl"

# =======================
# 📐 FAISS index config
# =======================
DIM = 1536
TOP_K = 3
SCORE_THRESHOLD = None

INDEX_NAME = "index_flat_L2.index"
INDEX_OUTPUT_PATH = PROJECT_ROOT / "storage/faiss" / INDEX_NAME
METADATA_OUTPUT_PATH = PROJECT_ROOT / "storage/faiss/metadata.jsonl"

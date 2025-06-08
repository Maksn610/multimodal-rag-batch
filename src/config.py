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
# 🔐 EMBEDDING
# =======================
EMBED_MODEL = "text-embedding-3-small"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# =======================
# 📂 DATA PATHS
# =======================
RAW_DIR = Path("data")
IMAGES_DIR = RAW_DIR / "images"
JSONL_DIR = RAW_DIR / "jsonl"
INDEX_OUTPUT_PATH = Path("storage/faiss/index_flat_L2.index")
METADATA_OUTPUT_PATH = Path("storage/faiss/metadata.jsonl")

# =======================
# 📐 FAISS CONFIG
# =======================
DIM = 1536
TOP_K = 3
SCORE_THRESHOLD = None

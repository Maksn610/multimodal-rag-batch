import json
import logging
import numpy as np
from pathlib import Path
from typing import List, Union
from dataclasses import asdict
from src.indexing.schema import ArticleMeta

logger = logging.getLogger(__name__)

# FAISS fallback for Windows
try:
    from faiss import IndexFlatL2, write_index
except ImportError:
    from faiss.swigfaiss_avx2 import IndexFlatL2, write_index


def build_faiss_index(vectors: List[np.ndarray], dim: int) -> IndexFlatL2:
    if not vectors:
        raise ValueError("No vectors provided for index building.")
    index: IndexFlatL2 = IndexFlatL2(dim)
    index.add(np.vstack(vectors))
    logger.info(f"FAISS index created with {len(vectors)} vectors of dim {dim}")
    return index


def save_index(index: IndexFlatL2, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_index(index, str(path))
    logger.info(f"FAISS index saved to: {path}")


def save_metadata(metadata: List[Union[dict, ArticleMeta]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for entry in metadata:
            data = asdict(entry) if hasattr(entry, "__dataclass_fields__") else entry
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    logger.info(f"Metadata saved to: {path} ({len(metadata)} entries)")

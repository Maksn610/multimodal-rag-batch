import numpy as np
from pathlib import Path
import json
from typing import List, Dict, Any

# FAISS fallback for Windows faiss-cpu
try:
    from faiss import IndexFlatL2, write_index
except ImportError:
    from faiss.swigfaiss_avx2 import IndexFlatL2, write_index


def build_faiss_index(vectors: List[np.ndarray], dim: int):
    index = IndexFlatL2(dim)
    index.add(np.vstack(vectors))
    return index


def save_index(index, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_index(index, str(path))


def save_metadata(metadata: List[Dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for entry in metadata:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

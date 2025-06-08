import numpy as np
from pathlib import Path
import json
from typing import List, Union
from dataclasses import asdict
from indexing.faiss_backend.schema import ArticleMeta

# FAISS fallback for Windows faiss-cpu
try:
    from faiss import IndexFlatL2, write_index
except ImportError:
    from faiss.swigfaiss_avx2 import IndexFlatL2, write_index


def build_faiss_index(vectors: List[np.ndarray], dim: int) -> IndexFlatL2:
    index: IndexFlatL2 = IndexFlatL2(dim)
    index.add(np.vstack(vectors))
    return index


def save_index(index: IndexFlatL2, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_index(index, str(path))


def save_metadata(metadata: List[Union[dict, ArticleMeta]], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        for entry in metadata:
            data = asdict(entry) if hasattr(entry, "__dataclass_fields__") else entry
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

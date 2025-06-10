import numpy as np
from src.embedding.embedding_client import get_embedding


def test_embedding_output_shape():
    text = "Test query for embedding"
    embedding = get_embedding(text)

    assert isinstance(embedding, np.ndarray)
    assert embedding.ndim == 1
    assert embedding.shape[0] > 0

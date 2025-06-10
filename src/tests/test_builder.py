import json
from pathlib import Path
from src.embedding.builder import run_embedding_pipeline
from src.config import EMBED_CACHE_PATH

def test_embedding_pipeline_skips_cached(monkeypatch, tmp_path):
    test_id = "dummy_id_1"
    EMBED_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    EMBED_CACHE_PATH.write_text(json.dumps({"id": test_id, "title": "Dummy"}) + "\n", encoding="utf-8")

    monkeypatch.setattr("src.embedding.embedding_client.get_embedding", lambda _: [0.1] * 1536)

    monkeypatch.setattr("src.utils.io_utils.load_articles", lambda _: [{"issue_id": "issue_999", "title": "Dummy", "text_blocks": []}])

    run_embedding_pipeline()

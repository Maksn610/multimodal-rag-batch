from search.search_engine import search, load_index, load_metadata
from config import INDEX_OUTPUT_PATH, METADATA_OUTPUT_PATH

def test_search_returns_valid_results():
    index = load_index(INDEX_OUTPUT_PATH)
    metadata = load_metadata(METADATA_OUTPUT_PATH)
    query = "Reasoning in vectors"

    results = search(query, index, metadata, top_k=3)

    assert isinstance(results, list)
    assert len(results) > 0
    for result in results:
        assert "title" in result
        assert "score" in result
        assert isinstance(result["score"], float)

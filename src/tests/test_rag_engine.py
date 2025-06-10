from src.rag.rag_engine import answer_query_multimodal


def test_answer_query_smoke():
    result = answer_query_multimodal("What is multimodal RAG?")
    assert isinstance(result, dict)
    assert "answer" in result
    assert "articles" in result

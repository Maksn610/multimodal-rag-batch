from src.rag.rag_engine import answer_query

def test_answer_query_smoke():
    result = answer_query("What is multimodal RAG?")
    assert isinstance(result, dict)
    assert "answer" in result
    assert "articles" in result

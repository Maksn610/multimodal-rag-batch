import logging
from typing import Dict
from pathlib import Path

from src.rag.llm_client import call_llm_multimodal
from src.search.search_engine import search_to_json

logger = logging.getLogger(__name__)
MAX_RESULTS = 3


def answer_query_multimodal(user_query: str) -> Dict:
    """
    Executes the full RAG pipeline using multimodal context (text + images + alt-texts).
    """
    logger.info("Running semantic search...")
    retrieved = search_to_json(user_query)
    if not retrieved:
        logger.warning("No relevant articles found.")
        return {
            "answer": "Sorry, I couldn't find any relevant articles.",
            "articles": []
        }

    top_article = retrieved[0]

    text = top_article.get("full_text", "")
    image_paths = [
        str(Path("data") / p) for p in top_article.get("local_image_paths", [])
    ]
    alt_texts = top_article.get("alt_texts", [])

    logger.info("Calling LLM with multimodal context (text + images + alt-texts)...")
    try:
        response = call_llm_multimodal(text, image_paths, alt_texts)
    except Exception as e:
        logger.exception("Multimodal call failed")
        return {
            "answer": "Error: unable to generate an answer.",
            "articles": retrieved
        }

    return {
        "answer": response,
        "articles": retrieved[:MAX_RESULTS]
    }

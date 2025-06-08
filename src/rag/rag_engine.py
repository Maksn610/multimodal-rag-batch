import logging
from typing import Dict, List

from src.rag.llm_client import call_llm
from src.rag.prompt_utils import build_prompt
from src.search.search_engine import search_to_json

logger = logging.getLogger(__name__)


def answer_query(user_query: str) -> Dict:
    """
    Handles the full RAG pipeline: search → prompt → LLM → return.

    Args:
        user_query (str): Input question from user.

    Returns:
        Dict: {
            "answer": LLM response,
            "articles": list of matched articles with metadata
        }
    """
    # Step 1: Retrieve top relevant articles
    retrieved = search_to_json(user_query)
    if not retrieved:
        return {
            "answer": "Sorry, I couldn't find relevant articles.",
            "articles": []
        }

    # Step 2: Build prompt from retrieved context
    prompt = build_prompt(user_query, retrieved)

    # Step 3: Get LLM response
    try:
        response = call_llm(prompt)
    except Exception as e:
        logger.exception("LLM call failed")
        return {
            "answer": "Sorry, something went wrong while generating a response.",
            "articles": retrieved
        }

    return {
        "answer": response,
        "articles": retrieved
    }

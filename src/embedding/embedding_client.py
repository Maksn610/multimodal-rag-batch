import time
import numpy as np
import logging
from openai import OpenAI, OpenAIError
from src.config import OPENAI_API_KEY, EMBED_MODEL

logger = logging.getLogger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)


def get_embedding(text: str, retries: int = 3, timeout: int = 10) -> np.ndarray:
    """
    Generate embedding for given text using OpenAI API with retries and timeout.

    Args:
        text (str): Input text.
        retries (int): Number of retry attempts.
        timeout (int): Timeout in seconds for API call.

    Returns:
        np.ndarray: Embedding vector.

    Raises:
        RuntimeError: If all retry attempts fail.
    """
    for attempt in range(retries):
        try:
            response = client.embeddings.create(
                input=text,
                model=EMBED_MODEL,
                timeout=timeout
            )
            return np.array(response.data[0].embedding, dtype=np.float32)
        except OpenAIError as e:
            wait_time = 2 ** attempt
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

    logger.exception(f"Failed to get embedding after {retries} attempts.")
    raise RuntimeError(f"Failed to get embedding after {retries} attempts.")

import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = "text-embedding-3-small"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def get_embedding(text: str) -> np.ndarray:
    """
    Generate embedding for given text using OpenAI API.

    Args:
        text (str): Input text.

    Returns:
        np.ndarray: Embedding vector.
    """
    response = client.embeddings.create(input=text, model=EMBED_MODEL)
    return np.array(response.data[0].embedding, dtype=np.float32)

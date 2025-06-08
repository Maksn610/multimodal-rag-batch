import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
SYSTEM_PROMPT = "You are a helpful AI assistant. Use only the provided context."

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY is not set in environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)


def call_llm(prompt: str) -> str:
    """
    Calls OpenAI chat model with a given prompt.

    Args:
        prompt (str): The input prompt including user query and context.

    Returns:
        str: The LLM's response text.
    """
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return "Error: LLM failed to respond."

import os
import logging
import base64
import json
from openai import OpenAI
from dotenv import load_dotenv
from typing import List

load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")  # обов'язково gpt-4o
SYSTEM_PROMPT = (
    "You are a helpful AI assistant. You are given:\n"
    "- the full text of an article,\n"
    "- its associated images (as base64), and\n"
    "- a list of alt-texts that describe these images.\n\n"
    "Your task is to analyze all of these inputs and produce a detailed, well-structured answer to the user's question.\n\n"
    "Guidelines:\n"
    "1. Use both the article text and the images to build your answer.\n"
    "2. Always include relevant facts or numbers found in the text. Quote from the article where appropriate.\n"
    "3. Always include references to the images. For example: 'In the accompanying image, we see...'\n"
    "4. Include details from the alt-texts when they help interpret what’s in the image.\n"
    "5. Do not invent information. Base your answer only on the provided context.\n"
    "6. The more specific and complete your answer is, the better.\n\n"
    "Example:\n"
    "**User query:** What does the chart in the article show?\n"
    "**Text excerpt:** The article compares model accuracy over time.\n"
    "**Alt-text:** A line chart showing GPT-3 (83%), GPT-3.5 (89%), GPT-4 (94%)\n"
    "**Image:** A line chart with 3 plotted points.\n"
    "**Expected response:** In the accompanying image, we see a line chart comparing model accuracy. GPT-4 performs the best at 94%, followed by GPT-3.5 (89%) and GPT-3 (83%). This confirms the article's statement that newer models consistently improve accuracy."
)


if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY is not set.")

client = OpenAI(api_key=OPENAI_API_KEY)
last_payload = None


def build_multimodal_content(text: str, image_paths: List[str], alt_texts: List[str] = None) -> List[dict]:
    full_text = text
    if alt_texts:
        full_text += "\n\nDescriptions of associated images:\n"
        full_text += "\n".join(f"- {desc}" for desc in alt_texts)

    content = [{"type": "text", "text": full_text}]

    for img_path in image_paths:
        with open(img_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}
            })

    return content


def call_llm_multimodal(text: str, image_paths: List[str], alt_texts: List[str] = None) -> str:
    global last_payload
    try:
        content = build_multimodal_content(text, image_paths, alt_texts)
        last_payload = content

        logger.info("[LLM INPUT] system prompt:")
        logger.info(SYSTEM_PROMPT)
        logger.info("[LLM INPUT] user content:")
        logger.info(json.dumps(content, indent=2)[:5000])

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.exception(f"Multimodal LLM call failed: {e}")
        return "Error: failed to process multimodal input."

from typing import List, Dict


def build_prompt(user_query: str, results: List[Dict]) -> str:
    """
    Constructs a prompt for LLM using retrieved articles.

    Args:
        user_query (str): The user's original search query.
        results (List[Dict]): Retrieved articles with metadata.

    Returns:
        str: Prompt string for the LLM.
    """
    context_blocks = []
    for item in results:
        title = item.get("title", "Untitled")
        snippet = item.get("text_snippet", "").strip()
        images = item.get("local_image_paths", [])

        block = f"### Article: {title}\n{snippet}"
        if images:
            image_list = "\n".join(f"- {path}" for path in images)
            block += f"\n\nImages:\n{image_list}"

        context_blocks.append(block)

    context = "\n\n".join(context_blocks)

    prompt = (
        "You are given a user query and a set of articles from an AI newsletter. "
        "Each article may contain images. Based only on the content below, answer the query concisely.\n\n"
        f"=== USER QUERY ===\n{user_query}\n\n"
        f"=== CONTEXT ===\n{context}\n\n"
        "=== RESPONSE ==="
    )

    return prompt

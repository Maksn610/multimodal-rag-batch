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

        block = f"### Article: {title}\n"
        block += f"{snippet}\n"

        if images:
            block += "\nImages:\n"
            for path in images:
                block += f"- {path}\n"

        context_blocks.append(block)

    context = "\n\n".join(context_blocks)

    prompt = (
        f"You are given a user query and a set of articles from an AI newsletter. "
        f"Each article may contain images. Based only on the content below, answer the query concisely.\n\n"
        f"=== USER QUERY ===\n{user_query}\n\n"
        f"=== CONTEXT ===\n{context}\n\n"
        f"=== RESPONSE ==="
    )

    return prompt

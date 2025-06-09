from typing import List, Dict


def build_prompt(user_query: str, results: List[Dict]) -> str:
    context_blocks = []
    for item in results:
        title = item.get("title", "Untitled")
        full_text = item.get("full_text", "").strip()
        images = item.get("local_image_paths", [])
        alt_texts = item.get("alt_texts", [])

        block = f"### Article: {title}\n{full_text}"

        if alt_texts:
            alt_list = "\n".join(f"- {text}" for text in alt_texts)
            block += f"\n\nAlt-texts:\n{alt_list}"

        if images:
            image_list = "\n".join(f"- {path}" for path in images)
            block += f"\n\nImages:\n{image_list}"

        context_blocks.append(block)

    context = "\n\n".join(context_blocks)

    prompt = (
        "You are a helpful AI assistant. Based only on the articles below, "
        "answer the user's question in detail. Use all relevant information from the context, "
        "including any image descriptions if helpful. Be clear and informative.\n\n"
        f"=== USER QUERY ===\n{user_query}\n\n"
        f"=== CONTEXT ===\n{context}\n\n"
        "=== RESPONSE ==="
    )

    return prompt

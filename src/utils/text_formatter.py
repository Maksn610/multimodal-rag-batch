def prepare_text(article: dict) -> str:
    """
    Prepares a text representation of the article by concatenating its title,
    main text blocks, and alt-texts for images.

    Args:
        article (dict): Article dictionary with 'text_blocks' and 'title'.

    Returns:
        str: Formatted text for embedding.
    """
    text_blocks = " ".join([tb["text"] for tb in article["text_blocks"] if tb["type"] == "text"])
    alt_texts = " ".join([tb["text"] for tb in article["text_blocks"] if tb["type"] == "alt_text"])
    return f"{article['title']}\n\n{text_blocks}\n\n{alt_texts}"

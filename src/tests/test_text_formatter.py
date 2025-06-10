from src.utils.text_formatter import prepare_text

def test_prepare_text_basic():
    article = {
        "title": "Test Title",
        "text_blocks": [
            {"type": "text", "text": "Main content here."},
            {"type": "alt_text", "text": "Image alt description."}
        ]
    }
    result = prepare_text(article)
    assert "Test Title" in result
    assert "Main content here." in result
    assert "Image alt description." in result
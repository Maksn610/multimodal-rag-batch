import hashlib

def generate_article_id(issue_id: str, title: str) -> str:
    raw = f"{issue_id}_{title}".encode("utf-8")
    return hashlib.md5(raw).hexdigest()

from dataclasses import dataclass, asdict
from typing import List


@dataclass
class ArticleMeta:
    id: int
    title: str
    text_snippet: str
    full_text: str
    local_image_paths: List[str]

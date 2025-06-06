import os
import requests
from urllib.parse import urljoin, urlparse
from .url_utils import clean_url


def download_and_store_image(raw_src: str, issue_number: int, image_subdir: str) -> dict | None:
    try:
        if "url=" in raw_src:
            parsed_url = clean_url(raw_src.split("url=")[-1])
        else:
            parsed_url = raw_src

        full_url = parsed_url if parsed_url.startswith("http") else urljoin(f"https://www.deeplearning.ai/the-batch/issue-{issue_number}/", parsed_url)
        image_name = os.path.basename(urlparse(full_url).path)
        local_path = os.path.join(image_subdir, image_name)

        response = requests.get(full_url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            return {
                "url": full_url,
                "local_path": os.path.relpath(local_path, "data").replace("\\", "/")
            }

    except Exception:
        return None

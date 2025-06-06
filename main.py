import os
import time
from playwright.sync_api import sync_playwright, TimeoutError
from crawler.page_loader import load_issue_page, extract_issue_date
from parser.article_parser import extract_articles
from storage.json_writer import write_issue_json

START_ISSUE = 290
END_ISSUE = 285
OUTPUT_DIR = "data"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        for issue_number in range(START_ISSUE, END_ISSUE - 1, -1):
            output_path = os.path.join(OUTPUT_DIR, f"issue_{issue_number}.json")
            if os.path.exists(output_path):
                print(f"Issue {issue_number} already exists. Skipping.")
                continue

            url = f"https://www.deeplearning.ai/the-batch/issue-{issue_number}/"
            try:
                print(f"Processing issue {issue_number}...")
                if not load_issue_page(page, url):
                    print(f"Issue {issue_number} not found.")
                    continue

                issue_title = page.title().strip()
                issue_date = extract_issue_date(page)
                articles = extract_articles(page, issue_number)

                output_data = {
                    "issue_id": f"issue_{issue_number}",
                    "issue_title": issue_title,
                    "issue_url": url,
                    "issue_date": issue_date,
                    "articles": articles
                }

                write_issue_json(output_data, output_path)
                print(f"Issue {issue_number} saved.")
                time.sleep(1)

            except TimeoutError:
                print(f"Issue {issue_number} failed to load (timeout).")
            except Exception as e:
                print(f"Error with issue {issue_number}: {e}")

        browser.close()


if __name__ == "__main__":
    main()

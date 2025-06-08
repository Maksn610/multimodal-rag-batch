import logging
from src.search.search_engine import search_to_json, pretty_print_results

def run():
    logging.basicConfig(level=logging.INFO)
    query = input("🔍 Enter your search query: ")
    results = search_to_json(query)
    pretty_print_results(results)

if __name__ == "__main__":
    run()

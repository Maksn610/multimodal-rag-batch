import logging
from src.ingestion.workflow import run_ingestion
from src.embedding.builder import run_embedding_pipeline
from src.search.search_engine import search_to_json, pretty_print_results

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)

    # Step 1: Crawl and extract issues
    run_ingestion()
    logger.info("All issues parsed. Starting embedding and indexing...")

    # Step 2: Generate embeddings and build index
    run_embedding_pipeline()
    logger.info("Embedding pipeline completed.")

    # Step 3: Search interaction
    query = input("🔍 Enter your search query: ")
    results = search_to_json(query)
    pretty_print_results(results)


if __name__ == "__main__":
    main()

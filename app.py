import logging
from src.ingestion.workflow import run_ingestion
from src.embedding.builder import run_embedding_pipeline

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    run_ingestion()
    logger.info("All issues parsed. Starting embedding and indexing...")
    run_embedding_pipeline()


if __name__ == "__main__":
    main()

import logging
import subprocess
from pathlib import Path
from src.ingestion.workflow import run_ingestion
from src.embedding.builder import run_embedding_pipeline
import subprocess

subprocess.run(["playwright", "install"], check=True)
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)

    logger.info("Starting ingestion...")
    run_ingestion()

    logger.info("Generating embeddings and building index...")
    run_embedding_pipeline()

    logger.info("Launching Streamlit UI...")
    try:
        ui_path = Path(__file__).parent / "src" / "app" / "rag_ui.py"
        if not ui_path.exists():
            logger.error(f"UI script not found: {ui_path}")
            return
        subprocess.run(["streamlit", "run", str(ui_path.resolve())], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to launch Streamlit: {e}")


if __name__ == "__main__":
    main()

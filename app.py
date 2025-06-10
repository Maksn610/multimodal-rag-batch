import logging
import subprocess
from pathlib import Path
import os

from src.ingestion.workflow import run_ingestion
from src.embedding.builder import run_embedding_pipeline

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)

    logger.info("Starting ingestion...")
    run_ingestion()

    logger.info("Generating embeddings and building index...")
    run_embedding_pipeline()

    logger.info("Launching Streamlit UI...")

    project_root = Path(__file__).parent
    ui_path = project_root / "src" / "ui" / "rag_ui.py"

    if not ui_path.exists():
        logger.error(f"UI script not found: {ui_path}")
        return

    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)

    try:
        subprocess.run(
            ["streamlit", "run", str(ui_path.resolve())],
            check=True,
            cwd=str(project_root),
            env=env
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to launch Streamlit: {e}")


if __name__ == "__main__":
    main()

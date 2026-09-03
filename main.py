import logging

from src.config.logger import setup_logging
from src.orchestrator import orchestrator

setup_logging()
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Iniciando processo de ETL ...")
    orchestrator()
    logger.info("Processo de ETL finalizado com sucesso ...")


if __name__ == "__main__":
    main()

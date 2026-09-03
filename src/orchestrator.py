import logging
from pathlib import Path

from src.etl.extract.extract import extract_leitos
from src.etl.load.load import load_tables
from src.etl.transform.transform import transform_leitos
from src.etl.validate.validate import validate_leitos

logger = logging.getLogger(__name__)


def orchestrator() -> None:
    # Extract
    logger.info("Iniciando Extração do CSV")
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "data/raw/leitos/Leitos_2026.csv"
    df = extract_leitos(file_path)
    logger.info(f"LINHAS: {df.shape[0]:,}")
    logger.info(f"COLUNAS: {df.shape[1]}")
    logger.info("Fim da Extração do CSV")

    # Validate
    logger.info("Iniciando validação dos dados no DF")
    validate_leitos(df)
    logger.info("Dados validados com sucesso")

    # Transform
    logger.info("iniciando transformação dos dados")
    data = transform_leitos(df)
    logger.info("Transformação dos dados concluidas com sucesso")

    # Load
    logger.info("Iniciando carga das tabelas")
    load_tables(data)
    # logger.info(data["dim_tempo"].head())
    # logger.info(data["dim_localidade"].head())
    # logger.info(data["dim_estabelecimento"].head())
    # logger.info(data["fact"].head())
    logger.info("Carga das tabelas concluida")

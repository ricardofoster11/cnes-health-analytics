import logging
from pathlib import Path

import pandas as pd

from src.config.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def execute_profiling():
    files = {
        # "estabelecimentos": BASE_DIR
        # / "data/raw/estabelecimentos/cnes_estabelecimentos.csv",
        "leitos": BASE_DIR / "data/raw/leitos/Leitos_2026.csv"
    }

    for name, file_path in files.items():
        logger.info(f"ARQUIVO: {name}")
        logger.info(f"CAMINHO: {file_path}")

        df = pd.read_csv(
            file_path,
            sep=";",
            encoding="latin1",
            low_memory=False
        )

        logger.info(f"LINHAS: {df.shape[0]:,}")
        logger.info(f"COLUNAS: {df.shape[1]}")

        # for column in df.columns:
        #     logger.info(column)

        for column in df.columns:
            if pd.api.types.is_string_dtype(df[column]):
                max_size = df[column].str.len().max()
            else:
                max_size = 0

            logger.info(f"{column} | TIPO: {df[column].dtype} | MAX: {max_size}")

        logger.info("PRIMEIROS REGISTROS:")
        logger.info(df.head())

        logger.info("NULOS:")
        logger.info(df.isnull().sum().sort_values(ascending=False).head(20))

        logger.info("LINHAS DUPLICADAS:")
        logger.info(df.duplicated().sum())

        logger.info("COMPETÊNCIAS:")
        logger.info(df["COMP"].value_counts().sort_index())

        logger.info("QUANTIDADE DE CNES ÚNICOS:")
        logger.info(df["CNES"].nunique())

        logger.info("REGISTROS POR UF:")
        logger.info(df["UF"].value_counts().sort_index())

        logger.info("CNES + COMP DUPLICADOS:")
        logger.info(df.duplicated(subset=["CNES", "COMP"]).sum())

        logger.info("CNES + DIFERENTES EM SP:")        
        logger.info(df.loc[df["UF"] == "SP", "CNES"].nunique())

        logger.info("TAMANHO MAXIMO: NOME_ESTABELECIMENTO")
        logger.info(df["NOME_ESTABELECIMENTO"].str.len().max())

        logger.info("TAMANHO MAXIMO: NOME_ESTABELECIMENTO")
        logger.info(df["NOME_ESTABELECIMENTO"].str.len().max())

        logger.info("=============")


if __name__ == "__main__":
    logger.info("Iniciando profiling")

    execute_profiling()

    logger.info("Profiling concluido")

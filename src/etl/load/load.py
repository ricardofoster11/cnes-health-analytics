import logging

import pandas as pd
from sqlalchemy import text

from src.database.connection import create_database_engine

logger = logging.getLogger(__name__)


def truncate_tables() -> None:
    engine = create_database_engine()

    logger.info("Limpando dados das tabelas")

    query = """
    TRUNCATE TABLE
        fact_capacidade_hospitalar,
        dim_estabelecimento,
        dim_localidade,
        dim_tempo
    RESTART IDENTITY CASCADE;
    """

    try:
        with engine.begin() as connection:
            connection.execute(text(query))

        logger.info("Tabelas limpas com sucesso")

    except Exception:
        logger.exception("Erro ao limpar as tabelas")
        raise
    finally:
        engine.dispose()


def load_dim_tempo(df: pd.DataFrame) -> None:
    logger.info("Alimentando a Tabela: dim_tempo")

    engine = create_database_engine()

    try:
        df.to_sql(
            name="dim_tempo",
            con=engine,
            if_exists="append",
            index=False
        )

        logger.info("Carga da dim_tempo concluída")

    except Exception:
        logger.exception("Erro na carga da dim_tempo")
        raise
    finally:
        engine.dispose()


def load_dim_localidade(df: pd.DataFrame) -> None:
    logger.info("Alimentando a Tabela: dim_localidade")

    engine = create_database_engine()

    try:
        df.to_sql(
            name="dim_localidade",
            con=engine,
            if_exists="append",
            index=False
        )

        logger.info("Carga da dim_localidade concluída")

    except Exception:
        logger.exception("Erro na carga da dim_localidade")
        raise
    finally:
        engine.dispose()


def load_dim_estabelecimento(df: pd.DataFrame) -> None:
    logger.info("Alimentando a Tabela: dim_estabelecimento")

    engine = create_database_engine()

    try:
        df.to_sql(
            name="dim_estabelecimento",
            con=engine,
            if_exists="append",
            index=False
        )

        logger.info("Carga da dim_estabelecimento concluída")

    except Exception:
        logger.exception("Erro na carga da dim_estabelecimento")
        raise
    finally:
        engine.dispose()


"""
Calculo Data Fact + Dados Tabela
"""


def get_dim_tempo_ids() -> pd.DataFrame:
    engine = create_database_engine()

    try:
        query = """
        SELECT
            id_tempo,
            comp
        FROM dim_tempo;
        """

        return pd.read_sql(query, engine)
    finally:
        engine.dispose()


def get_dim_estabelecimento_ids() -> pd.DataFrame:
    engine = create_database_engine()

    try:
        query = """
        SELECT
            id_estabelecimento,
            cnes
        FROM dim_estabelecimento;
        """

        return pd.read_sql(query, engine)
    finally:
        engine.dispose()


def get_dim_localidade_ids() -> pd.DataFrame:
    engine = create_database_engine()

    try:
        query = """
        SELECT
            id_localidade,
            co_ibge
        FROM dim_localidade;
        """

        return pd.read_sql(query, engine)
    finally:
        engine.dispose()


def load_fact_capacidade_hospitalar(df: pd.DataFrame) -> None:
    logger.info("Iniciando fact_capacidade_hospitalar")

    engine = create_database_engine()

    try:
        dim_tempo = get_dim_tempo_ids()
        dim_estabelecimento = get_dim_estabelecimento_ids()
        dim_localidade = get_dim_localidade_ids()

        fact = df.merge(
            dim_tempo,
            on="comp",
            how="left",
        )

        fact = fact.merge(
            dim_estabelecimento,
            on="cnes",
            how="left",
        )

        fact = fact.merge(
            dim_localidade,
            on="co_ibge",
            how="left",
        )

        if fact[
            [
                "id_tempo",
                "id_estabelecimento",
                "id_localidade",
            ]
        ].isnull().any().any():
            raise ValueError(
                "Existem registros da fato sem correspondência nas dimensões."
            )

        fact = fact.drop(
            columns=[
                "comp",
                "cnes",
                "co_ibge",
            ]
        )

        fact.to_sql(
            name="fact_capacidade_hospitalar",
            con=engine,
            if_exists="append",
            index=False,
        )

        logger.info(
            "Carga da fact_capacidade_hospitalar concluída"
        )
    except Exception:
        logger.exception(
            "Erro na carga da fact_capacidade_hospitalar"
        )
        raise
    finally:
        engine.dispose()


def load_tables(data: dict[str, pd.DataFrame]) -> None:
    truncate_tables()
    load_dim_tempo(data["dim_tempo"])
    load_dim_localidade(data["dim_localidade"])
    load_dim_estabelecimento(data["dim_estabelecimento"])
    load_fact_capacidade_hospitalar(data["fact"])

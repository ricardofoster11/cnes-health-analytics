import logging

from sqlalchemy import text

from src.config.logger import setup_logging
from src.database.connection import create_database_engine

setup_logging()
logger = logging.getLogger(__name__)


def create_table_estabelecimento() -> None:
    logger.info("Tabela dim_estabelecimento")
    engine = create_database_engine()

    query = """
    CREATE TABLE IF NOT EXISTS dim_estabelecimento (
        id_estabelecimento INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        cnes VARCHAR(7) UNIQUE NOT NULL,
        nome_estabelecimento VARCHAR(100),
        razao_social VARCHAR(100),
        tp_gestao CHAR(1),
        co_tipo_unidade INTEGER,
        ds_tipo_unidade VARCHAR(100),
        natureza_juridica INTEGER,
        desc_natureza_juridica VARCHAR(150),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );    
    """

    try:
        with engine.begin() as connection:
            connection.execute(text(query))
    finally:
        engine.dispose()


def create_table_localidade() -> None:
    logger.info("Tabela dim_localidade")
    engine = create_database_engine()

    query = """
    CREATE TABLE IF NOT EXISTS dim_localidade (
        id_localidade INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        co_ibge varchar(6) UNIQUE NOT NULL,
        regiao VARCHAR(30),
        uf CHAR(2),
        municipio VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        with engine.begin() as connection:
            connection.execute(text(query))
    finally:
        engine.dispose()


def create_table_tempo() -> None:
    logger.info("Tabela dim_tempo")
    engine = create_database_engine()

    query = """
    CREATE TABLE IF NOT EXISTS dim_tempo (
        id_tempo INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        comp INTEGER UNIQUE NOT NULL,
        ano INTEGER,
        mes INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        with engine.begin() as connection:
            connection.execute(text(query))
    finally:
        engine.dispose()


def create_table_capacidade_hospitalar() -> None:
    logger.info("Tabela fact_capacidade_hospitalar")
    engine = create_database_engine()

    query = """
    CREATE TABLE IF NOT EXISTS fact_capacidade_hospitalar (
        id_tempo INTEGER NOT NULL,
        id_estabelecimento INTEGER NOT NULL,
        id_localidade INTEGER NOT NULL,

        leitos_existentes INTEGER,
        leitos_sus INTEGER,
        leitos_nao_sus_calc INTEGER,

        uti_total_exist INTEGER,
        uti_total_sus INTEGER,
        uti_total_nao_sus_calc INTEGER,

        uti_adulto_exist INTEGER,
        uti_adulto_sus INTEGER,
        uti_adulto_nao_sus_calc INTEGER,

        uti_pediatrico_exist INTEGER,
        uti_pediatrico_sus INTEGER,
        uti_pediatrico_nao_sus_calc INTEGER,

        uti_neonatal_exist INTEGER,
        uti_neonatal_sus INTEGER,
        uti_neonatal_nao_sus_calc INTEGER,

        uti_queimado_exist INTEGER,
        uti_queimado_sus INTEGER,
        uti_queimado_nao_sus_calc INTEGER,

        uti_coronariana_exist INTEGER,
        uti_coronariana_sus INTEGER,
        uti_coronariana_nao_sus_calc INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT fk_capacidade_tempo
            FOREIGN KEY (id_tempo)
            REFERENCES dim_tempo(id_tempo),

        CONSTRAINT fk_capacidade_estabelecimento
            FOREIGN KEY (id_estabelecimento)
            REFERENCES dim_estabelecimento(id_estabelecimento),

        CONSTRAINT fk_capacidade_localidade
            FOREIGN KEY (id_localidade)
            REFERENCES dim_localidade(id_localidade),

        CONSTRAINT uq_capacidade_estabelecimento_tempo
            UNIQUE (id_estabelecimento, id_tempo)
    );
    """

    try:
        with engine.begin() as connection:
            connection.execute(text(query))
    finally:
        engine.dispose()


def create_database_structure() -> None:
    logger.info("Iniciando criação da estrutura do banco")

    create_table_estabelecimento()
    create_table_localidade()
    create_table_tempo()
    create_table_capacidade_hospitalar()

    logger.info("Estrutura do banco criada")


if __name__ == "__main__":
    create_database_structure()

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

load_dotenv()


def create_database_engine() -> Engine:
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    required_variables = {
        "POSTGRES_HOST": host,
        "POSTGRES_PORT": port,
        "POSTGRES_DB": database,
        "POSTGRES_USER": user,
        "POSTGRES_PASSWORD": password
    }

    for variable_name, variable_value in required_variables.items():
        if not variable_value:
            raise RuntimeError(
                f"A variável {variable_name} não foi configurada."
            )

    database_url = (
        f"postgresql+psycopg2://{user}:{password}"
        f"@{host}:{port}/{database}"
    )

    return create_engine(database_url)

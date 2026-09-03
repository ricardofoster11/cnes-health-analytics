import logging

import pandas as pd

logger = logging.getLogger(__name__)


def validate_leitos(df: pd.DataFrame) -> None:
    required_columns = {
        "COMP",
        "CNES",
        "CO_IBGE",
        "LEITOS_EXISTENTES",
        "LEITOS_SUS",
        "UTI_TOTAL_EXIST",
        "UTI_TOTAL_SUS",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Colunas obrigatórias ausentes: {missing_columns}"
        )

    if df.empty:
        raise ValueError("Dataset de leitos está vazio.")

    if df[["CNES", "COMP"]].isnull().any().any():
        raise ValueError("Existem valores nulos em CNES ou COMP.")

    if df.duplicated(subset=["CNES", "COMP"]).any():
        raise ValueError("Existem registros duplicados para CNES + COMP.")

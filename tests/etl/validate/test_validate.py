import pandas as pd
import pytest

from src.etl.validate.validate import validate_leitos


def build_validate_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "COMP": [202601],
            "CNES": [27],
            "CO_IBGE": [355030],
            "LEITOS_EXISTENTES": [100],
            "LEITOS_SUS": [70],
            "UTI_TOTAL_EXIST": [20],
            "UTI_TOTAL_SUS": [12],
        }
    )


def test_validate_leitos_valid_df():
    df = build_validate_df()

    validate_leitos(df)


def test_validate_leitos_missing_required_column():
    df = build_validate_df()

    df = df.drop(columns=["CNES"])

    with pytest.raises(
        ValueError,
        match="Colunas obrigatórias ausentes:"
    ):
        validate_leitos(df)


def test_validate_leitos_empty_df():
    df = build_validate_df()

    df = df.iloc[0:0]

    with pytest.raises(
        ValueError,
        match="Dataset de leitos está vazio."
    ):
        validate_leitos(df)


def test_validate_leitos_null_cnes():
    df = build_validate_df()

    df.loc[0, "CNES"] = None

    with pytest.raises(
        ValueError,
        match="Existem valores nulos em CNES ou COMP."
    ):
        validate_leitos(df)


def test_validate_leitos_null_comp():
    df = build_validate_df()

    df.loc[0, "COMP"] = None

    with pytest.raises(
        ValueError,
        match="Existem valores nulos em CNES ou COMP."
    ):
        validate_leitos(df)


def test_validate_leitos_duplicate_cnes_comp():
    df = build_validate_df()

    df = pd.concat([df, df], ignore_index=True)

    with pytest.raises(
        ValueError,
        match=r"Existem registros duplicados para CNES \+ COMP\."
    ):
        validate_leitos(df)

import pandas as pd
import pytest

import src.etl.load.load as load_module


def build_fact_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "comp": [202601],
            "cnes": ["0000027"],
            "co_ibge": ["355030"],
            "leitos_existentes": [100],
            "leitos_sus": [70],
            "leitos_nao_sus_calc": [30]
        }
    )


def build_dim_tempo() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id_tempo": [1],
            "comp": [202601],
        }
    )


def build_dim_estabelecimento() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id_estabelecimento": [10],
            "cnes": ["0000027"],
        }
    )


def build_dim_localidade() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id_localidade": [20],
            "co_ibge": ["355030"],
        }
    )


class FakeEngine:
    def dispose(self):
        pass


def test_load_fact_capacidade_hospitalar(monkeypatch):
    df = build_fact_df()

    monkeypatch.setattr(
        load_module,
        "create_database_engine",
        lambda: FakeEngine(),
    )

    monkeypatch.setattr(
        load_module,
        "get_dim_tempo_ids",
        build_dim_tempo,
    )

    monkeypatch.setattr(
        load_module,
        "get_dim_estabelecimento_ids",
        build_dim_estabelecimento,
    )

    monkeypatch.setattr(
        load_module,
        "get_dim_localidade_ids",
        build_dim_localidade,
    )

    captured = {}

    def fake_to_sql(self, name, con, if_exists, index):
        captured["df"] = self.copy()
        captured["name"] = name
        captured["if_exists"] = if_exists
        captured["index"] = index

    monkeypatch.setattr(
        pd.DataFrame,
        "to_sql",
        fake_to_sql,
    )

    load_module.load_fact_capacidade_hospitalar(df)

    fact_loaded = captured["df"]

    assert fact_loaded.iloc[0]["id_tempo"] == 1
    assert fact_loaded.iloc[0]["id_estabelecimento"] == 10
    assert fact_loaded.iloc[0]["id_localidade"] == 20

    assert "comp" not in fact_loaded.columns
    assert "cnes" not in fact_loaded.columns
    assert "co_ibge" not in fact_loaded.columns

    assert captured["name"] == "fact_capacidade_hospitalar"
    assert captured["if_exists"] == "append"
    assert captured["index"] is False


def test_load_fact_sem_correspondencia_dimensao(monkeypatch):
    df = build_fact_df()

    monkeypatch.setattr(
        load_module,
        "create_database_engine",
        lambda: FakeEngine(),
    )

    monkeypatch.setattr(
        load_module,
        "get_dim_tempo_ids",
        build_dim_tempo,
    )

    monkeypatch.setattr(
        load_module,
        "get_dim_estabelecimento_ids",
        build_dim_estabelecimento,
    )

    monkeypatch.setattr(
        load_module,
        "get_dim_localidade_ids",
        lambda: pd.DataFrame(
            {
                "id_localidade": [20],
                "co_ibge": ["999999"],
            }
        ),
    )

    with pytest.raises(
        ValueError,
        match="Existem registros da fato sem correspondência nas dimensões."
    ):
        load_module.load_fact_capacidade_hospitalar(df)

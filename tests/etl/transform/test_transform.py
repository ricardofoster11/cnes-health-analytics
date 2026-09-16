import pandas as pd

from src.etl.transform.transform import transform_leitos


def build_test_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "COMP": [202601],
            "CO_IBGE": [355030],
            "REGIAO": ["SUDESTE"],
            "UF": ["SP"],
            "MUNICIPIO": ["DIADEMA"],
            "CNES": [27],
            "NOME_ESTABELECIMENTO": ["Hospital Teste"],
            "RAZAO_SOCIAL": ["Hospital Teste LTDA"],
            "TP_GESTAO": ["M"],
            "CO_TIPO_UNIDADE": [5],
            "DS_TIPO_UNIDADE": ["HOSPITAL GERAL"],
            "NATUREZA_JURIDICA": [1000],
            "DESC_NATUREZA_JURIDICA": ["TESTE"],
            "LEITOS_EXISTENTES": [100],
            "LEITOS_SUS": [70],
            "UTI_TOTAL_EXIST": [20],
            "UTI_TOTAL_SUS": [12],
            "UTI_ADULTO_EXIST": [10],
            "UTI_ADULTO_SUS": [6],
            "UTI_PEDIATRICO_EXIST": [4],
            "UTI_PEDIATRICO_SUS": [2],
            "UTI_NEONATAL_EXIST": [3],
            "UTI_NEONATAL_SUS": [2],
            "UTI_QUEIMADO_EXIST": [1],
            "UTI_QUEIMADO_SUS": [1],
            "UTI_CORONARIANA_EXIST": [2],
            "UTI_CORONARIANA_SUS": [1],
        }
    )


def build_test_df_duplicates() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "COMP": [202603, 202601, 202601],
            "CO_IBGE": [355030, 355030, 330455],
            "REGIAO": ["SUDESTE", "SUDESTE", "SUDESTE"],
            "UF": ["SP", "SP", "RJ"],
            "MUNICIPIO": ["DIADEMA", "DIADEMA", "RIO DE JANEIRO"],
            "CNES": [27, 27, 99],
            "NOME_ESTABELECIMENTO": [
                "Hospital Teste",
                "Hospital Teste",
                "Hospital Rio",
            ],
            "RAZAO_SOCIAL": [
                "Hospital Teste LTDA",
                "Hospital Teste LTDA",
                "Hospital Rio LTDA",
            ],
            "TP_GESTAO": ["M", "M", "M"],
            "CO_TIPO_UNIDADE": [5, 5, 5],
            "DS_TIPO_UNIDADE": [
                "HOSPITAL GERAL",
                "HOSPITAL GERAL",
                "HOSPITAL GERAL",
            ],
            "NATUREZA_JURIDICA": [1000, 1000, 1000],
            "DESC_NATUREZA_JURIDICA": ["TESTE", "TESTE", "TESTE"],
            "LEITOS_EXISTENTES": [100, 100, 80],
            "LEITOS_SUS": [70, 70, 50],
            "UTI_TOTAL_EXIST": [20, 20, 10],
            "UTI_TOTAL_SUS": [12, 12, 6],
            "UTI_ADULTO_EXIST": [10, 10, 5],
            "UTI_ADULTO_SUS": [6, 6, 3],
            "UTI_PEDIATRICO_EXIST": [4, 4, 2],
            "UTI_PEDIATRICO_SUS": [2, 2, 1],
            "UTI_NEONATAL_EXIST": [3, 3, 1],
            "UTI_NEONATAL_SUS": [2, 2, 1],
            "UTI_QUEIMADO_EXIST": [1, 1, 1],
            "UTI_QUEIMADO_SUS": [1, 1, 0],
            "UTI_CORONARIANA_EXIST": [2, 2, 1],
            "UTI_CORONARIANA_SUS": [1, 1, 1],
        }
    )


def test_transform_leitos_dim_tempo():
    df = build_test_df()

    result = transform_leitos(df)

    dim_tempo = result["dim_tempo"]

    assert dim_tempo.iloc[0]["comp"] == 202601
    assert dim_tempo.iloc[0]["ano"] == 2026
    assert dim_tempo.iloc[0]["mes"] == 1


def test_transform_leitos_dim_localidade():
    df = build_test_df()

    result = transform_leitos(df)

    dim_localidade = result["dim_localidade"]

    assert dim_localidade.iloc[0]["co_ibge"] == "355030"
    assert dim_localidade.iloc[0]["regiao"] == "SUDESTE"
    assert dim_localidade.iloc[0]["uf"] == "SP"
    assert dim_localidade.iloc[0]["municipio"] == "DIADEMA"
    assert dim_localidade.iloc[0]["estado"] == "São Paulo"
    assert dim_localidade.iloc[0]["localizacao"] == "DIADEMA, São Paulo, Brasil"


def test_transform_leitos_dim_estabelecimento():
    df = build_test_df()

    result = transform_leitos(df)

    dim_estabelecimento = result["dim_estabelecimento"]

    assert dim_estabelecimento.iloc[0]["cnes"] == "0000027"
    assert dim_estabelecimento.iloc[0]["nome_estabelecimento"] == "Hospital Teste"
    assert dim_estabelecimento.iloc[0]["razao_social"] == "Hospital Teste LTDA"
    assert dim_estabelecimento.iloc[0]["tp_gestao"] == "M"
    assert dim_estabelecimento.iloc[0]["co_tipo_unidade"] == 5
    assert dim_estabelecimento.iloc[0]["ds_tipo_unidade"] == "HOSPITAL GERAL"
    assert dim_estabelecimento.iloc[0]["natureza_juridica"] == 1000
    assert dim_estabelecimento.iloc[0]["desc_natureza_juridica"] == "TESTE"


def test_transform_fact():
    df = build_test_df()

    result = transform_leitos(df)

    fact = result["fact"]

    assert fact.iloc[0]["comp"] == 202601
    assert fact.iloc[0]["cnes"] == "0000027"
    assert fact.iloc[0]["co_ibge"] == "355030"
    assert fact.iloc[0]["leitos_existentes"] == 100
    assert fact.iloc[0]["leitos_sus"] == 70
    assert fact.iloc[0]["leitos_nao_sus_calc"] == 30
    assert fact.iloc[0]["uti_total_exist"] == 20
    assert fact.iloc[0]["uti_total_sus"] == 12
    assert fact.iloc[0]["uti_total_nao_sus_calc"] == 8
    assert fact.iloc[0]["uti_adulto_exist"] == 10
    assert fact.iloc[0]["uti_adulto_sus"] == 6
    assert fact.iloc[0]["uti_adulto_nao_sus_calc"] == 4
    assert fact.iloc[0]["uti_pediatrico_exist"] == 4
    assert fact.iloc[0]["uti_pediatrico_sus"] == 2
    assert fact.iloc[0]["uti_pediatrico_nao_sus_calc"] == 2
    assert fact.iloc[0]["uti_neonatal_exist"] == 3
    assert fact.iloc[0]["uti_neonatal_sus"] == 2
    assert fact.iloc[0]["uti_neonatal_nao_sus_calc"] == 1
    assert fact.iloc[0]["uti_queimado_exist"] == 1
    assert fact.iloc[0]["uti_queimado_sus"] == 1
    assert fact.iloc[0]["uti_queimado_nao_sus_calc"] == 0
    assert fact.iloc[0]["uti_coronariana_exist"] == 2
    assert fact.iloc[0]["uti_coronariana_sus"] == 1
    assert fact.iloc[0]["uti_coronariana_nao_sus_calc"] == 1


def test_transform_leitos_duplicates_and_sort():
    df = build_test_df_duplicates()

    result = transform_leitos(df)

    dim_tempo = result["dim_tempo"]
    dim_localidade = result["dim_localidade"]
    dim_estabelecimento = result["dim_estabelecimento"]

    assert len(dim_tempo) == 2
    assert len(dim_localidade) == 2
    assert len(dim_estabelecimento) == 2

    assert dim_tempo.iloc[0]["comp"] == 202601
    assert dim_tempo.iloc[1]["comp"] == 202603

    assert dim_localidade.iloc[0]["co_ibge"] == "330455"
    assert dim_localidade.iloc[1]["co_ibge"] == "355030"

    assert dim_estabelecimento.iloc[0]["cnes"] == "0000027"
    assert dim_estabelecimento.iloc[1]["cnes"] == "0000099"

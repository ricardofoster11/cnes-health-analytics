import logging

import pandas as pd

logger = logging.getLogger(__name__)


def transform_leitos(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    logger.info("Iniciando transform dim_tempo")

    dim_tempo = (
        df[["COMP"]]
        .drop_duplicates()
        .copy()
    )

    dim_tempo["ano"] = (
        dim_tempo["COMP"]
        .astype(str)
        .str[:4]
        .astype(int)
    )

    dim_tempo["mes"] = (
        dim_tempo["COMP"]
        .astype(str)
        .str[4:6]
        .astype(int)
    )

    dim_tempo = dim_tempo.rename(
        columns={
            "COMP": "comp"
        }
    )

    dim_tempo = dim_tempo.sort_values("comp")

    logger.info("Transform dim_tempo concluido")
    logger.info("Iniciando transform dim_localidade")

    dim_localidade = (
        df[["CO_IBGE", "REGIAO", "UF", "MUNICIPIO"]]
        .drop_duplicates(subset=["CO_IBGE"])
        .copy()
    )

    dim_localidade["CO_IBGE"] = (
        dim_localidade["CO_IBGE"]
        .astype(str)
        .str.zfill(6)
    )

    dim_localidade = dim_localidade.rename(
        columns={
            "CO_IBGE": "co_ibge",
            "REGIAO": "regiao",
            "UF": "uf",
            "MUNICIPIO": "municipio"
        }
    )

    dim_localidade = dim_localidade.sort_values("co_ibge")

    logger.info("Transform dim_localidade concluido")
    logger.info("Iniciando transform dim_estabelecimento")

    dim_estabelecimento = (
        df[
            [
                "CNES",
                "NOME_ESTABELECIMENTO",
                "RAZAO_SOCIAL",
                "TP_GESTAO",
                "CO_TIPO_UNIDADE",
                "DS_TIPO_UNIDADE",
                "NATUREZA_JURIDICA",
                "DESC_NATUREZA_JURIDICA",
            ]
        ]
        .drop_duplicates(subset=["CNES"])
        .copy()
    )

    dim_estabelecimento["CNES"] = (
        dim_estabelecimento["CNES"]
        .astype(str)
        .str.zfill(7)
    )

    dim_estabelecimento = dim_estabelecimento.rename(
        columns={
            "CNES": "cnes",
            "NOME_ESTABELECIMENTO": "nome_estabelecimento",
            "RAZAO_SOCIAL": "razao_social",
            "TP_GESTAO": "tp_gestao",
            "CO_TIPO_UNIDADE": "co_tipo_unidade",
            "DS_TIPO_UNIDADE": "ds_tipo_unidade",
            "NATUREZA_JURIDICA": "natureza_juridica",
            "DESC_NATUREZA_JURIDICA": "desc_natureza_juridica",
        }
    )

    dim_estabelecimento = dim_estabelecimento.sort_values("cnes")

    logger.info("Transform dim_estabelecimento concluido")
    logger.info("Iniciando transform fact_capacidade_hospitalar")

    fact = df[
        [
            "COMP",
            "CNES",
            "CO_IBGE",
            "LEITOS_EXISTENTES",
            "LEITOS_SUS",
            "UTI_TOTAL_EXIST",
            "UTI_TOTAL_SUS",
            "UTI_ADULTO_EXIST",
            "UTI_ADULTO_SUS",
            "UTI_PEDIATRICO_EXIST",
            "UTI_PEDIATRICO_SUS",
            "UTI_NEONATAL_EXIST",
            "UTI_NEONATAL_SUS",
            "UTI_QUEIMADO_EXIST",
            "UTI_QUEIMADO_SUS",
            "UTI_CORONARIANA_EXIST",
            "UTI_CORONARIANA_SUS",
        ]
    ].copy()

    fact["CNES"] = (
        fact["CNES"]
        .astype(str)
        .str.zfill(7)
    )

    fact["CO_IBGE"] = (
        fact["CO_IBGE"]
        .astype(str)
        .str.zfill(6)
    )

    fact["LEITOS_NAO_SUS_CALC"] = (
        fact["LEITOS_EXISTENTES"] - fact["LEITOS_SUS"]
    )

    fact["UTI_TOTAL_NAO_SUS_CALC"] = (
        fact["UTI_TOTAL_EXIST"] - fact["UTI_TOTAL_SUS"]
    )

    fact["UTI_ADULTO_NAO_SUS_CALC"] = (
        fact["UTI_ADULTO_EXIST"] - fact["UTI_ADULTO_SUS"]
    )

    fact["UTI_PEDIATRICO_NAO_SUS_CALC"] = (
        fact["UTI_PEDIATRICO_EXIST"] - fact["UTI_PEDIATRICO_SUS"]
    )

    fact["UTI_NEONATAL_NAO_SUS_CALC"] = (
        fact["UTI_NEONATAL_EXIST"] - fact["UTI_NEONATAL_SUS"]
    )

    fact["UTI_QUEIMADO_NAO_SUS_CALC"] = (
        fact["UTI_QUEIMADO_EXIST"] - fact["UTI_QUEIMADO_SUS"]
    )

    fact["UTI_CORONARIANA_NAO_SUS_CALC"] = (
        fact["UTI_CORONARIANA_EXIST"] - fact["UTI_CORONARIANA_SUS"]
    )

    fact = fact[
        [
            "COMP",
            "CNES",
            "CO_IBGE",

            "LEITOS_EXISTENTES",
            "LEITOS_SUS",
            "LEITOS_NAO_SUS_CALC",

            "UTI_TOTAL_EXIST",
            "UTI_TOTAL_SUS",
            "UTI_TOTAL_NAO_SUS_CALC",

            "UTI_ADULTO_EXIST",
            "UTI_ADULTO_SUS",
            "UTI_ADULTO_NAO_SUS_CALC",

            "UTI_PEDIATRICO_EXIST",
            "UTI_PEDIATRICO_SUS",
            "UTI_PEDIATRICO_NAO_SUS_CALC",

            "UTI_NEONATAL_EXIST",
            "UTI_NEONATAL_SUS",
            "UTI_NEONATAL_NAO_SUS_CALC",

            "UTI_QUEIMADO_EXIST",
            "UTI_QUEIMADO_SUS",
            "UTI_QUEIMADO_NAO_SUS_CALC",

            "UTI_CORONARIANA_EXIST",
            "UTI_CORONARIANA_SUS",
            "UTI_CORONARIANA_NAO_SUS_CALC",
        ]
    ]

    fact = fact.rename(
        columns={
            "COMP": "comp",
            "CNES": "cnes",
            "CO_IBGE": "co_ibge",
            "LEITOS_EXISTENTES": "leitos_existentes",
            "LEITOS_SUS": "leitos_sus",
            "LEITOS_NAO_SUS_CALC": "leitos_nao_sus_calc",
            "UTI_TOTAL_EXIST": "uti_total_exist",
            "UTI_TOTAL_SUS": "uti_total_sus",
            "UTI_TOTAL_NAO_SUS_CALC": "uti_total_nao_sus_calc",
            "UTI_ADULTO_EXIST": "uti_adulto_exist",
            "UTI_ADULTO_SUS": "uti_adulto_sus",
            "UTI_ADULTO_NAO_SUS_CALC": "uti_adulto_nao_sus_calc",
            "UTI_PEDIATRICO_EXIST": "uti_pediatrico_exist",
            "UTI_PEDIATRICO_SUS": "uti_pediatrico_sus",
            "UTI_PEDIATRICO_NAO_SUS_CALC": "uti_pediatrico_nao_sus_calc",
            "UTI_NEONATAL_EXIST": "uti_neonatal_exist",
            "UTI_NEONATAL_SUS": "uti_neonatal_sus",
            "UTI_NEONATAL_NAO_SUS_CALC": "uti_neonatal_nao_sus_calc",
            "UTI_QUEIMADO_EXIST": "uti_queimado_exist",
            "UTI_QUEIMADO_SUS": "uti_queimado_sus",
            "UTI_QUEIMADO_NAO_SUS_CALC": "uti_queimado_nao_sus_calc",
            "UTI_CORONARIANA_EXIST": "uti_coronariana_exist",
            "UTI_CORONARIANA_SUS": "uti_coronariana_sus",
            "UTI_CORONARIANA_NAO_SUS_CALC": "uti_coronariana_nao_sus_calc",
        }
    )

    logger.info("Transform fact_capacidade_hospitalar concluido")

    return {
        "dim_tempo": dim_tempo,
        "dim_localidade": dim_localidade,
        "dim_estabelecimento": dim_estabelecimento,
        "fact": fact,
    }

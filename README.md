# cnes-health-analytics

Projeto de Engenharia e Análise de Dados desenvolvido para explorar dados públicos de saúde do Cadastro Nacional de Estabelecimentos de Saúde (CNES).

O projeto implementa um pipeline ETL para extração, validação, transformação e carga de dados de estabelecimentos de saúde, leitos hospitalares e UTIs em um banco PostgreSQL.

## Objetivo

Construir uma base analítica para análise da capacidade hospitalar brasileira, permitindo explorar informações como:

* quantidade de leitos existentes;
* quantidade de leitos disponíveis ao SUS;
* quantidade calculada de leitos não SUS;
* capacidade de UTIs;
* distribuição por tipo de UTI;
* distribuição geográfica por região, UF e município;
* evolução da capacidade hospitalar por competência.

## Fonte dos dados

Os dados utilizados são públicos e disponibilizados pelo Ministério da Saúde por meio do CNES.

Arquivos utilizados:

* `cnes_estabelecimentos.csv`
* `Leitos_2026.csv`

Os arquivos brutos não são versionados neste repositório e devem ser armazenados localmente em:

```text
data/
└── raw/
    ├── estabelecimentos/
    │   └── cnes_estabelecimentos.csv
    └── leitos/
        └── Leitos_2026.csv
```

## Pipeline ETL

O processamento foi dividido em quatro etapas principais:

```text
Extract
   ↓
Validate
   ↓
Transform
   ↓
Load
   ↓
PostgreSQL
```

### Extract

Responsável pela leitura dos arquivos CSV e disponibilização dos dados em DataFrames Pandas.

### Validate

Executa validações de qualidade e estrutura dos dados antes do processamento, incluindo:

* existência das colunas obrigatórias;
* dataset vazio;
* valores nulos em campos críticos;
* duplicidade da combinação `CNES + COMP`.

### Transform

Responsável pela preparação dos dados para o modelo analítico.

Entre as principais transformações estão:

* padronização de CNES e código IBGE;
* criação das dimensões;
* derivação de ano e mês a partir da competência;
* cálculo de leitos não SUS;
* cálculo de UTIs não SUS;
* padronização dos nomes das colunas.

### Load

Responsável pela carga dos dados no PostgreSQL.

As dimensões são carregadas primeiro e suas chaves são posteriormente associadas aos registros da tabela fato.

A carga segue a ordem:

```text
dim_tempo
   ↓
dim_localidade
   ↓
dim_estabelecimento
   ↓
fact_capacidade_hospitalar
```

## Modelo de Dados

O banco utiliza uma modelagem dimensional composta por três dimensões e uma tabela fato.

### dim_tempo

Representa as competências disponíveis no dataset.

Principais atributos:

* `id_tempo`
* `comp`
* `ano`
* `mes`

### dim_localidade

Representa a localização dos estabelecimentos.

Principais atributos:

* `id_localidade`
* `co_ibge`
* `regiao`
* `uf`
* `municipio`

### dim_estabelecimento

Contém os dados cadastrais dos estabelecimentos de saúde.

Principais atributos:

* `id_estabelecimento`
* `cnes`
* `nome_estabelecimento`
* `razao_social`
* `tp_gestao`
* `co_tipo_unidade`
* `ds_tipo_unidade`
* `natureza_juridica`
* `desc_natureza_juridica`

### fact_capacidade_hospitalar

Armazena as medidas relacionadas à capacidade hospitalar por estabelecimento e competência.

Entre as principais métricas estão:

* leitos existentes;
* leitos SUS;
* leitos não SUS calculados;
* UTIs existentes;
* UTIs SUS;
* UTIs não SUS calculadas;
* UTI adulto;
* UTI pediátrica;
* UTI neonatal;
* UTI para queimados;
* UTI coronariana.

A granularidade da tabela fato é:

> **um registro por estabelecimento (CNES) e competência.**

## Tecnologias

* Python
* Pandas
* SQLAlchemy
* PostgreSQL
* Docker
* Git

## Estrutura do projeto

```text
src/
├── config/
├── database/
├── etl/
│   ├── extract/
│   ├── validate/
│   ├── transform/
│   └── load/
└── profiling/
```

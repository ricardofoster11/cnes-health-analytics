-- ============================================================
-- CNES Health Analytics
-- Validation Queries
-- ============================================================
-- Queries utilizadas para validar os dados carregados no
-- PostgreSQL e conferir os indicadores apresentados no Power BI.
-- ============================================================


-- ------------------------------------------------------------
-- 1. Amostra da tabela fato com suas dimensões
-- ------------------------------------------------------------

SELECT
    dt.comp,
    dl.uf,
    dl.municipio,
    de.cnes,
    de.nome_estabelecimento,
    fch.leitos_existentes,
    fch.leitos_sus,
    fch.leitos_nao_sus_calc
FROM fact_capacidade_hospitalar fch
INNER JOIN dim_tempo dt
    ON dt.id_tempo = fch.id_tempo
INNER JOIN dim_localidade dl
    ON dl.id_localidade = fch.id_localidade
INNER JOIN dim_estabelecimento de
    ON de.id_estabelecimento = fch.id_estabelecimento
LIMIT 20;


-- ------------------------------------------------------------
-- 2. Estabelecimentos por competência
-- ------------------------------------------------------------

SELECT
    id_tempo,
    COUNT(DISTINCT id_estabelecimento) AS total_estabelecimentos
FROM fact_capacidade_hospitalar
GROUP BY id_tempo
ORDER BY id_tempo;


-- ------------------------------------------------------------
-- 3. Total de leitos por competência
-- ------------------------------------------------------------

SELECT
    id_tempo,
    SUM(leitos_existentes) AS total_leitos
FROM fact_capacidade_hospitalar
GROUP BY id_tempo
ORDER BY id_tempo;


-- ------------------------------------------------------------
-- 4. Total de leitos SUS por competência
-- ------------------------------------------------------------

SELECT
    id_tempo,
    SUM(leitos_sus) AS total_leitos_sus
FROM fact_capacidade_hospitalar
GROUP BY id_tempo
ORDER BY id_tempo;


-- ------------------------------------------------------------
-- 5. Percentual de leitos SUS
-- ------------------------------------------------------------

SELECT
    id_tempo,
    SUM(leitos_sus) * 100.0
        / SUM(leitos_existentes) AS percentual_sus
FROM fact_capacidade_hospitalar
GROUP BY id_tempo
ORDER BY id_tempo;


-- ------------------------------------------------------------
-- 6. Municípios atendidos
-- ------------------------------------------------------------

SELECT
    id_tempo,
    COUNT(DISTINCT id_localidade) AS municipios_atendidos
FROM fact_capacidade_hospitalar
GROUP BY id_tempo
ORDER BY id_tempo;


-- ------------------------------------------------------------
-- 7. Estabelecimentos por UF
-- ------------------------------------------------------------

SELECT
    dl.uf,
    COUNT(DISTINCT fch.id_estabelecimento) AS total_estabelecimentos
FROM fact_capacidade_hospitalar fch
INNER JOIN dim_localidade dl
    ON dl.id_localidade = fch.id_localidade
WHERE fch.id_tempo = 1
GROUP BY dl.uf
ORDER BY total_estabelecimentos DESC;


-- ------------------------------------------------------------
-- 8. Leitos de UTI existentes por tipo
-- ------------------------------------------------------------

SELECT
    id_tempo,
    SUM(uti_adulto_exist) AS adulto,
    SUM(uti_pediatrico_exist) AS pediatrico,
    SUM(uti_neonatal_exist) AS neonatal,
    SUM(uti_queimado_exist) AS queimado,
    SUM(uti_coronariana_exist) AS coronariana,
    SUM(uti_adulto_exist)
        + SUM(uti_pediatrico_exist)
        + SUM(uti_neonatal_exist)
        + SUM(uti_queimado_exist)
        + SUM(uti_coronariana_exist) AS total_uti
FROM fact_capacidade_hospitalar
GROUP BY id_tempo
ORDER BY id_tempo;
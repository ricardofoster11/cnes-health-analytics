-- ============================================================
-- CNES Health Analytics
-- Validation Queries
-- ============================================================
-- Queries utilizadas para validar os dados carregados no
-- PostgreSQL e conferir os indicadores apresentados no Power BI.
-- ============================================================

-- ------------------------------------------------------------
-- 1. Soma das utis sus
-- ------------------------------------------------------------

select fch.id_tempo
, sum(fch.uti_total_sus) as uti_sus
, sum(fch.uti_neonatal_sus) as uti_neonatal
, sum(fch.uti_pediatrico_sus) as uti_pediatrico
, sum(fch.uti_adulto_sus) as uti_adulto
, sum(fch.uti_coronariana_sus) as uti_coronariana
, sum(fch.uti_queimado_sus) as uti_queimado  
from fact_capacidade_hospitalar fch 
where fch.id_tempo = 1
group by fch.id_tempo 
order by 1

-- ------------------------------------------------------------
-- 2. Soma sus e não sus
-- ------------------------------------------------------------

SELECT
    id_tempo,
    SUM(uti_total_exist) AS uti_existentes,
    SUM(uti_total_sus) AS uti_sus,
    SUM(uti_total_nao_sus_calc) AS uti_nao_sus
FROM fact_capacidade_hospitalar
GROUP BY id_tempo
ORDER BY id_tempo;

-- ------------------------------------------------------------
-- 3. sus por uf
-- ------------------------------------------------------------
SELECT
    dl.estado,
    SUM(fch.uti_total_sus) AS uti_sus
FROM fact_capacidade_hospitalar fch
INNER JOIN dim_localidade dl
    ON dl.id_localidade = fch.id_localidade
WHERE fch.id_tempo = 3
GROUP BY dl.estado
ORDER BY uti_sus DESC;
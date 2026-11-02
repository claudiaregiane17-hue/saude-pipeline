-- Mart 1: Indicadores gerais de saúde e custo hospitalar em MG (2025)
SELECT
    COUNT(*) AS total_internacoes,
    SUM(valor_total_hospitalar) AS faturamento_total,
    ROUND(AVG(valor_total_hospitalar), 2) AS custo_medio_internacao,
    ROUND(AVG(dias_permanencia), 1) AS permanencia_media_dias,
    ROUND(100.0 * SUM(flag_obito) / COUNT(*), 2) AS taxa_mortalidade_pct,
    ROUND(100.0 * COUNT(CASE WHEN valor_uti > 0 THEN 1 END) / COUNT(*), 2) AS pct_uso_uti
FROM refined_internacoes;

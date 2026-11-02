-- Mart 2: Evolução temporal de internações e gastos por mês
SELECT
    STRFTIME(data_internacao, '%Y-%m') AS mes_ano,
    COUNT(*) AS qtd_internacoes,
    ROUND(SUM(valor_total_hospitalar), 2) AS valor_total,
    ROUND(100.0 * SUM(flag_obito) / COUNT(*), 2) AS taxa_mortalidade_pct
FROM refined_internacoes
WHERE data_internacao >= '2025-01-01' AND data_internacao <= '2025-12-31'
GROUP BY 1
ORDER BY 1;

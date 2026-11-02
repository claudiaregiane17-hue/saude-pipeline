-- Mart 3: Principais causas de hospitalização com JOIN na dimensão CID-10
SELECT
    COALESCE(c.nome_capitulo, 'Outras Afecções') AS causa_internacao,
    COUNT(*) AS total_internacoes,
    ROUND(SUM(i.valor_total_hospitalar), 2) AS custo_total,
    ROUND(100.0 * SUM(i.flag_obito) / COUNT(*), 2) AS taxa_mortalidade_pct
FROM refined_internacoes i
LEFT JOIN read_parquet('data/raw/dim/capitulos_cid10.parquet') c
    ON i.cid_letra >= c.letra_inicio AND i.cid_letra <= c.letra_fim
GROUP BY 1
ORDER BY total_internacoes DESC;

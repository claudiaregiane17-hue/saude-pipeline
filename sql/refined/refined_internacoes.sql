-- Camada Refined: Limpeza e normalização dos microdados do SIH/MG (2025)
SELECT
    N_AIH AS id_internacao,
    UF_ZI AS uf,
    MUNIC_RES AS cod_municipio_residencia,
    -- Converte datas no formato YYYYMMDD para DATE de forma segura
    TRY_STRPTIME(CAST(DT_INTER AS VARCHAR), '%Y%m%d')::DATE AS data_internacao,
    TRY_STRPTIME(CAST(DT_SAIDA AS VARCHAR), '%Y%m%d')::DATE AS data_saida,
    -- Dias de internação (garantindo mínimo de 1 diária)
    GREATEST(
        (TRY_STRPTIME(CAST(DT_SAIDA AS VARCHAR), '%Y%m%d')::DATE - 
         TRY_STRPTIME(CAST(DT_INTER AS VARCHAR), '%Y%m%d')::DATE),
        1
    ) AS dias_permanencia,
    -- Diagnóstico e identificador do capítulo CID
    DIAG_PRINC AS cid_principal,
    SUBSTRING(CAST(DIAG_PRINC AS VARCHAR), 1, 1) AS cid_letra,
    -- Demografia
    TRY_CAST(IDADE AS INTEGER) AS idade,
    CASE 
        WHEN CAST(SEXO AS VARCHAR) = '1' THEN 'Masculino'
        WHEN CAST(SEXO AS VARCHAR) = '3' THEN 'Feminino'
        ELSE 'Não informado'
    END AS sexo,
    -- Tipo de saída (Morte = 1 se MORTE = '1', senão 0)
    CASE WHEN CAST(MORTE AS VARCHAR) = '1' THEN 1 ELSE 0 END AS flag_obito,
    -- Valores financeiros convertidos explicitamente para número
    TRY_CAST(VAL_TOT AS DOUBLE) AS valor_total_hospitalar,
    COALESCE(TRY_CAST(VAL_UTI AS DOUBLE), 0.0) AS valor_uti
FROM read_parquet('data/raw/sih/*.parquet')
WHERE TRY_STRPTIME(CAST(DT_INTER AS VARCHAR), '%Y%m%d') IS NOT NULL 
  AND TRY_STRPTIME(CAST(DT_SAIDA AS VARCHAR), '%Y%m%d') IS NOT NULL
  AND TRY_CAST(VAL_TOT AS DOUBLE) > 0;

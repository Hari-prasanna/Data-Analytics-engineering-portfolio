{{
    config(
        materialized = 'view'
    )
}}

WITH snapshot_data AS (
    SELECT *
    FROM {{ ref('accounts_snapshot') }}
)

SELECT 
    dbt_scd_id AS customer_sk,          
    account_natural_key AS customer_id, 
    risk_level,
    CASE 
        WHEN ROW_NUMBER() OVER (PARTITION BY account_natural_key ORDER BY dbt_valid_from ASC) = 1 
        THEN '1900-01-01 00:00:00'::timestamp 
        ELSE dbt_valid_from 
    END AS valid_from,
    
    dbt_valid_to AS valid_to,
    CASE WHEN dbt_valid_to IS NULL THEN TRUE ELSE FALSE END AS is_current

FROM snapshot_data
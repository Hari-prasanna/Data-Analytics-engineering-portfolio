WITH stg_transactions AS (SELECT *
FROM {{ref('stg_transactions')}}),


all_account AS (
SELECT 
    sender_account_id AS account_id,
    risk_level
FROM stg_transactions
UNION ALL
SELECT 
    receiver_account_id AS account_id,
    risk_level
FROM stg_transactions),


unique_account_id AS 
(SELECT 
    DISTINCT account_id,
    MAX(risk_level) as risk_level
FROM all_account
WHERE account_id IS NOT NULL
GROUP BY 1)

SELECT 
    {{dbt_utils.generate_surrogate_key(['account_id'])}} as customer_sk,
    account_id AS account_natural_key,
    risk_level
FROM unique_account_id

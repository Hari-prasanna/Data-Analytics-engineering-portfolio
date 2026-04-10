{% snapshot accounts_snapshot %}

{{
    config(
      target_schema='snapshots',
      strategy='check',
      unique_key='account_natural_key',
      check_cols=['risk_level', 'last_transaction_at'],
    )
}}

WITH all_accounts AS (
    SELECT 
        sender_account_id AS account_natural_key,
        risk_level,
        transaction_timestamp AS last_transaction_at
    FROM {{ ref('stg_transactions') }}

    UNION ALL

    SELECT 
        receiver_account_id AS account_natural_key,
        CASE WHEN transaction_amount > 10000 THEN 'HIGH_RISK' ELSE 'LOW_RISK' END AS risk_level,
        transaction_timestamp AS last_transaction_at
    FROM {{ ref('stg_transactions') }}
)

SELECT 
    account_natural_key,
    risk_level,
    MAX(last_transaction_at) AS last_transaction_at
FROM all_accounts
WHERE account_natural_key IS NOT NULL
GROUP BY 1, 2

{% endsnapshot %}
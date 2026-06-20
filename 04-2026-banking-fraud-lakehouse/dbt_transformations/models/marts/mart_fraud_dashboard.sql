{{
    config(
        materialized = 'table',
        description = 'Flat One Big Table (OBT) optimized for BI dashboards and Analyst ad-hoc queries.'
    )
}}

SELECT 
    f.transaction_id,
    f.transaction_timestamp,
    f.transaction_amount,
    f.transaction_type,
    f.is_fraud,
    f.is_flagged_fraud,
    f.is_zero_impact_txn,
    s.customer_id AS sender_account_id,
    s.risk_level AS sender_risk_level,
    f.sender_balance_error,
    r.customer_id AS receiver_account_id,
    r.risk_level AS receiver_risk_level,
    f.receiver_balance_error

FROM {{ ref('fct_transaction') }} f

LEFT JOIN {{ ref('dim_customers') }} s 
    ON f.sender_customer_sk = s.customer_sk
    
LEFT JOIN {{ ref('dim_customers') }} r 
    ON f.receiver_customer_sk = r.customer_sk
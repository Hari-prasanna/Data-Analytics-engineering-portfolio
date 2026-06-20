{{
    config(
        materialized = 'incremental',
        unique_key = 'transaction_id',
        incremental_strategy = 'merge'
    )
}}

SELECT 
    t.transaction_id,
    t.transaction_timestamp,
    
    c_sender.customer_sk AS sender_customer_sk,
    c_receiver.customer_sk AS receiver_customer_sk,
    
    t.transaction_amount,
    t.transaction_type,
    t.is_fraud,
    t.is_flagged_fraud,
    
    t.sender_balance_error,
    t.receiver_balance_error,
    t.is_zero_impact_txn

FROM {{ ref('stg_transactions') }} t

-- Time-Travel Join: Sender
LEFT JOIN {{ ref('dim_customers') }} c_sender
    ON t.sender_account_id = c_sender.customer_id
    AND t.transaction_timestamp >= c_sender.valid_from
    AND t.transaction_timestamp < COALESCE(c_sender.valid_to, '9999-12-31'::timestamp)

-- Time-Travel Join: Receiver
LEFT JOIN {{ ref('dim_customers') }} c_receiver
    ON t.receiver_account_id = c_receiver.customer_id
    AND t.transaction_timestamp >= c_receiver.valid_from
    AND t.transaction_timestamp < COALESCE(c_receiver.valid_to, '9999-12-31'::timestamp)


{% if is_incremental() %}
    WHERE t.transaction_timestamp >= (SELECT MAX(transaction_timestamp) - INTERVAL 72 HOURS FROM {{ this }})
{% endif %}
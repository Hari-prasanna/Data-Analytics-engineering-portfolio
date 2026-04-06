SELECT 
    t.transaction_id,
    c_sender.customer_sk AS sender_customer_sk,
    c_receiver.customer_sk AS receiver_customer_sk,
    t.sender_account_id,
    t.transaction_amount,
    t.transaction_type,
    t.step_hour,
    t.is_fraud
    
FROM {{ ref('stg_transactions') }} t

LEFT JOIN {{ ref('dim_customers') }} c_sender
    ON t.sender_account_id = c_sender.account_natural_key

LEFT JOIN {{ ref('dim_customers') }} c_receiver
    ON t.receiver_account_id = c_receiver.account_natural_key
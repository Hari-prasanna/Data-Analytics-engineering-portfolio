WITH raw_data AS (SELECT *
FROM {{source('fraud_analysis_data', 'raw_transactions')}}),

cleaned AS 
(SELECT
    CAST(step AS INT) AS step_hour,
    CAST(step AS INT) % 24 AS hour_of_day,
    CAST(type AS STRING) AS transaction_type,
    CAST(amount AS DOUBLE) AS transaction_amount,
        
    CAST(nameOrig AS STRING) AS sender_account_id,
    CAST(oldbalanceOrg AS DOUBLE) AS sender_old_balance,
    CAST(newbalanceOrig AS DOUBLE) AS sender_new_balance,
        
    CAST(nameDest AS STRING) AS receiver_account_id,
    CAST(oldbalanceDest AS DOUBLE) AS receiver_old_balance,
    CAST(newbalanceDest AS DOUBLE) AS receiver_new_balance,
        
    CAST(isFraud AS BOOLEAN) AS is_fraud,
    CAST(isFlaggedFraud AS BOOLEAN) AS is_flagged_fraud
FROM raw_data)


SELECT
    md5(concat(CAST(step_hour AS STRING), sender_account_id, receiver_account_id, CAST(transaction_amount AS STRING))) AS transaction_id,
    *,
    (CASE WHEN receiver_account_id LIKE 'M%' THEN TRUE
    ELSE FALSE
    END) AS is_receiver_merchant,
    ROUND((sender_new_balance + transaction_amount) - sender_old_balance,2) AS sender_balance_error,
    (CASE
      WHEN receiver_account_id LIKE 'M%' THEN 0
      ELSE ROUND((receiver_old_balance + transaction_amount) - receiver_new_balance,2)
      END)receiver_balance_error,
    (CASE
      WHEN sender_old_balance = sender_new_balance AND transaction_amount > 0 THEN TRUE ELSE FALSE END) AS is_zero_impact_txn
FROM cleaned


    
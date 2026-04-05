WITH raw_data AS (
    select * from {{source('fraud_analysis_data', 'raw_transactions')}}
),

renamed_and_casted AS (
    SELECT
        CAST(step AS INT) AS step_hour,
        CAST(type AS STRING) AS transaction_type,
        CAST(amount AS DOUBLE) AS transaction_amount,
        
        -- Origin Account Info
        CAST(nameOrig AS STRING) AS orig_account_id,
        CAST(oldbalanceOrg AS DOUBLE) AS orig_old_balance,
        CAST(newbalanceOrig AS DOUBLE) AS orig_new_balance,
        
        -- Destination Account Info
        CAST(nameDest AS STRING) AS dest_account_id,
        CAST(oldbalanceDest AS DOUBLE) AS dest_old_balance,
        CAST(newbalanceDest AS DOUBLE) AS dest_new_balance,
        
        -- Labels (Casting to BOOLEAN makes them easier to query downstream)
        CAST(isFraud AS BOOLEAN) AS is_fraud,
        CAST(isFlaggedFraud AS BOOLEAN) AS is_flagged_fraud
        
        -- Note: We intentionally drop _rescued_data here as it is an Auto Loader 
        -- artifact and not needed for business logic.
    FROM raw_data
),

engineered_features AS (
    SELECT 
        *,
        -- FEATURE 1: The "Merchant" Limitation Mask
        -- If the destination is a merchant, flag it as TRUE
        CASE 
            WHEN dest_account_id LIKE 'M%' THEN TRUE 
            ELSE FALSE 
        END AS is_merchant_dest,

        -- FEATURE 2: Logical Balance Errors
        -- Mathematically, these should perfectly equal $0$. 
        -- High deviations = massive red flags for the ML models.
        ROUND(
            (orig_new_balance + transaction_amount) - orig_old_balance, 2
        ) AS orig_balance_error,

        ROUND(
            (dest_old_balance + transaction_amount) - dest_new_balance, 2
        ) AS dest_balance_error

    FROM renamed_and_casted
)

SELECT * FROM engineered_features
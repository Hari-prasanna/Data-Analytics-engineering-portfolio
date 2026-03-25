{{ config(
    materialized='incremental',
    unique_key=['user_session', 'user_id'],
    incremental_strategy='merge'
) }}

WITH session_events AS (
    SELECT
        user_session,
        user_id,
        
        MIN(event_time) AS session_start_at,
        MAX(event_time) AS session_end_at,
        
        MAX(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS has_view,
        MAX(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS has_cart,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS has_purchase,
        
        SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS total_page_views,
        COUNT(DISTINCT CASE WHEN event_type = 'view' THEN product_id ELSE NULL END) AS unique_products_viewed,
        SUM(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS total_adds_to_cart,
        SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS total_purchases,
        
        SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) AS session_revenue
        
    FROM {{ ref('stg_raw_events') }}

    {% if is_incremental() %}
        WHERE user_session IN (
            SELECT DISTINCT user_session
            FROM {{ ref('stg_raw_events') }}
            WHERE event_time >= (
                SELECT MAX(session_end_at) - INTERVAL {{ var('lookback_days', 3) }} DAYS 
                FROM {{ this }}
            )
        )
    {% endif %}
    
    GROUP BY 
        user_session, user_id
)

SELECT
    *,
    CASE 
        WHEN has_cart = 1 AND has_purchase = 0 THEN TRUE 
        ELSE FALSE 
    END AS is_abandoned_cart
FROM session_events
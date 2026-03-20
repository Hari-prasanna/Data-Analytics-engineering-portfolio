{{config(materialized = 'table')}}

WITH source AS (SELECT *
FROM {{ref('stg_raw_events')}}),


user_session AS (SELECT 
    user_session,
    user_id,
    MIN(event_time) AS session_start_at,
    MAX(event_time) AS session_end_at,
    MAX(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS has_view,
    MAX(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS has_cart,
    MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS has_purchase,
    SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS total_views,
    SUM(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS total_adds_to_cart,
    SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS total_purchases,
    SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) AS session_revenue
FROM source
GROUP BY user_session,user_id)


SELECT *,
    CASE 
        WHEN has_cart = 1 AND has_purchase = 0 THEN TRUE 
        ELSE FALSE 
    END AS is_abandoned_cart
FROM user_session
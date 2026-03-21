{{config(materialized = 'table')}}

WITH source AS (SELECT *
FROM {{ref('stg_raw_events')}}),


product_events AS(

    SELECT
        product_id,
        SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS total_views,
        SUM(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS total_added_to_cart,
        SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS total_purchased,
        SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) AS product_revenue
    FROM source
    GROUP BY 
        product_id
)
SELECT
    product_id,
    total_views,
    total_added_to_cart,
    total_purchased,
    product_revenue,
    ROUND((CAST(total_purchased AS DECIMAL(10,4)) / NULLIF(total_views, 0)) * 100, 2) AS view_to_purchase_conversion_pct
FROM product_events

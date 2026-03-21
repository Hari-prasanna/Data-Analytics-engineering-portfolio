{{ config(materialized='table') }}

WITH latest_product_state AS (
    SELECT
        product_id,
        category_id,
        category,
        subcategory,
        subsubcategory,
        brand,
        price
    FROM {{ ref('stg_raw_events') }}
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY product_id 
        ORDER BY event_time DESC
    ) = 1
)

SELECT * FROM latest_product_state
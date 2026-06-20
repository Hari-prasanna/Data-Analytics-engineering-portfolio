{{ config(
    materialized='incremental',
    unique_key='event_id',
    incremental_strategy='merge'
) }}

WITH raw_data AS (
    SELECT
        md5(concat_ws('||', 
            COALESCE(user_session, ''), 
            COALESCE(CAST(user_id AS STRING), ''), 
            CAST(event_time AS STRING), 
            CAST(product_id AS STRING), 
            event_type
        )) AS event_id,
        
        CAST(event_time AS TIMESTAMP) AS event_time,
        event_type,
        CAST(product_id AS BIGINT) AS product_id,
        CAST(category_id AS BIGINT) AS category_id,
        get(SPLIT(category_code, '\\.'), 0) AS category,
        get(SPLIT(category_code, '\\.'), 1) AS subcategory,
        get(SPLIT(category_code, '\\.'), 2) AS subsubcategory,
        brand,
        CAST(price AS DECIMAL(10,2)) AS price,
        CAST(user_id AS BIGINT) AS user_id,
        user_session

    FROM {{ source('event_data', 'raw_events') }}
    WHERE event_time IS NOT NULL 
      AND user_id IS NOT NULL

    {% if is_incremental() %}
      AND CAST(event_time AS TIMESTAMP) >= (SELECT MAX(event_time) - INTERVAL 3 DAYS FROM {{ this }})
      
    {% endif %}
)

SELECT * FROM raw_data
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY event_id 
    ORDER BY event_time
) = 1
{{ config(materialized='view') }}


WITH raw_data AS (SELECT * 
FROM {{source('event_data','raw_events')}}),

cleaned AS (SELECT
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
    user_session,
    ROW_NUMBER() OVER(PARTITION BY user_session, user_id, event_time, product_id, event_type 
    ORDER BY event_time) AS rnk 
FROM raw_data
WHERE event_time IS NOT NULL 
AND user_id IS NOT NULL)


SELECT *
FROM cleaned
WHERE rnk = 1

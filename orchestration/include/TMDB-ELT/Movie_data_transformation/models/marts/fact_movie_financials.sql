{{ config(
    materialized='incremental',
    unique_key='movie_id'
) }}

WITH stg_raw_movie_details AS (
    SELECT *
    FROM {{ ref('stg_raw_movie_details') }}
),

cleaned AS (
    SELECT
        movie_id,
        budget,
        revenue,
        loaded_at,
        (revenue - budget) AS profit,
        CASE 
            WHEN budget > 0 THEN ROUND(((revenue - budget)::NUMERIC / budget) * 100, 2)
            ELSE NULL 
        END AS roi_percentage
    FROM stg_raw_movie_details
)

SELECT * FROM cleaned
{% if is_incremental() %}
    WHERE loaded_at > (SELECT MAX(loaded_at) FROM {{ this }})
{% endif %}
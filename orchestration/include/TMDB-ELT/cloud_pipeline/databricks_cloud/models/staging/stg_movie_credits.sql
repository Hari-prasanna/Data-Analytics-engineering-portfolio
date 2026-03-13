{{ config(
    materialized='incremental',
    unique_key=['movie_id', 'actor_id'] 
) }}

WITH raw_credits AS (
    SELECT * FROM {{ source('tmdb_bronze', 'raw_movie_credits') }}
),

deduplicated_movies AS (
    SELECT 
        cast(id as INT) AS movie_id,
        `cast` as cast_json_string, 
        cast(loaded_at as TIMESTAMP) AS loaded_at,
        ROW_NUMBER() OVER (PARTITION BY id ORDER BY loaded_at DESC) as row_num
    FROM raw_credits
    
    {% if is_incremental() %}
    WHERE loaded_at > (SELECT MAX(loaded_at) FROM {{ this }})
    {% endif %}
),

unpacked_cast AS (
    SELECT 
        movie_id,
        loaded_at,
        explode(from_json(cast_json_string, 'array<struct<id:int, name:string>>')) AS actor
    FROM deduplicated_movies
    WHERE row_num = 1 
      AND cast_json_string IS NOT NULL
),

cleaned_cast AS (
    SELECT
        movie_id,
        actor.id AS actor_id,
        actor.name AS actor_name,
        loaded_at
    FROM unpacked_cast
    WHERE actor.id IS NOT NULL
)

SELECT * FROM cleaned_cast
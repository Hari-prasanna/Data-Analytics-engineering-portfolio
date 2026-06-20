WITH raw_details AS (
    SELECT * FROM {{ source('tmdb_bronze', 'raw_movie_details') }}
),

unpacked_genres AS (
    SELECT 
        cast(id as INT) AS movie_id, 
        explode(from_json(genres, 'array<struct<id:int, name:string>>')) AS genre
    FROM raw_details
    WHERE genres IS NOT NULL 
)

SELECT 
    movie_id,
    genre.id AS genre_id 
FROM unpacked_genres
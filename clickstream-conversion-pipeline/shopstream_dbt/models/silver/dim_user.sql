{{ config(materialized = 'table') }}


WITH source AS (SELECT *
FROM {{ref('stg_raw_events')}})


SELECT
    user_id,
    MIN(event_time) AS first_active_at,
    MAX(event_time) AS last_active_at,
    COUNT(DISTINCT user_session) AS total_sessions_in_month
    FROM source
    GROUP BY user_id
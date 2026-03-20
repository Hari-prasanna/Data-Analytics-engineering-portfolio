{{config(materialized = 'table')}}

WITH source AS (SELECT *
FROM {{ref('fct_session_funnel')}})



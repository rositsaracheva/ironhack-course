-- ============================================================================
-- BrewBeats — Mini Project 2: Section D (dbt + Airflow Pipeline)
-- Folder: Section D - dbt + Airflow Pipeline/Section D_Q1/
-- Task  : Section D - Q1: Create a staging model in dbt for coffee_sales.
-- ============================================================================
-- What is a staging model in dbt and how does this query work?
-- A staging model (stg_coffee_sales) is the first cleaning layer in dbt. It takes the raw
-- 'coffee_sales' table and standardizes column names, data types, and missing values:
-- 1. WITH source AS (...): reads the raw table using dbt's {{ source('raw', 'coffee_sales') }} macro.
-- 2. ROW_NUMBER() OVER (ORDER BY datetime, coffee_name) AS transaction_id: generates a unique ID
--    for every coffee sale so we can test uniqueness on every row.
-- 3. CAST(date AS DATE) AS sale_date & CAST(datetime AS TIMESTAMP) AS sale_timestamp: ensures
--    our date and timestamp columns have clean Date/Timestamp data types.
-- 4. LOWER(TRIM(cash_type)) AS payment_type: cleans text formatting ('card' or 'cash').
-- 5. COALESCE(card, 'CASH_NO_CARD') AS card_id: replaces empty/NULL card values on cash transactions
--    with 'CASH_NO_CARD' so there are no unexpected NULLs.
-- 6. ROUND(CAST(money AS NUMERIC(10, 2)), 2) AS amount: casts 'money' to a 2-decimal currency number.
-- 7. TRIM(coffee_name) AS coffee_name: removes any accidental leading/trailing spaces from drink names.

with source as (

    select * from {{ source('raw', 'coffee_sales') }}

),

cleaned as (

    select
        row_number() over (order by datetime, coffee_name) as transaction_id,
        cast(date as date) as sale_date,
        cast(datetime as timestamp) as sale_timestamp,
        lower(trim(cash_type)) as payment_type,
        coalesce(card, 'CASH_NO_CARD') as card_id,
        round(cast(money as numeric(10, 2)), 2) as amount,
        trim(coffee_name) as coffee_name
    from source
    where date is not null
      and money > 0

)

select * from cleaned

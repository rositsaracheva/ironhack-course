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

/*
Verified Execution Output (`dbt run` — Section D - Q1):
-------------------------------------------------------
11:40:49  Running with dbt=1.13.0-b1
11:40:49  Registered adapter: duckdb=1.11.1
11:40:50  Found 2 models, 9 data tests, 1 source, 511 macros
11:40:50  
11:40:50  Concurrency: 4 threads (target='dev')
11:40:50  
11:40:50  1 of 2 START sql view model main.stg_coffee_sales .............................. [RUN]
11:40:50  1 of 2 OK created sql view model main.stg_coffee_sales ......................... [OK in 0.04s]
11:40:50  2 of 2 START sql table model main.fct_daily_revenue ............................ [RUN]
11:40:50  2 of 2 OK created sql table model main.fct_daily_revenue ....................... [OK in 0.04s]
11:40:50  
11:40:50  Finished running 1 table model, 1 view model in 0 hours 0 minutes and 0.15 seconds (0.15s).
11:40:50  
11:40:50  Completed successfully
11:40:50  
11:40:50  Done. PASS=2 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=2

--- Preview of stg_coffee_sales (Q1 Staging View - Top 5 Rows) ---
┌────────────────┬────────────┬─────────────────────────┬───┬─────────────────────┬───────────────┬───────────────┐
│ transaction_id │ sale_date  │     sale_timestamp      │ … │       card_id       │    amount     │  coffee_name  │
│     int64      │    date    │        timestamp        │ … │       varchar       │ decimal(10,2) │    varchar    │
├────────────────┼────────────┼─────────────────────────┼───┼─────────────────────┼───────────────┼───────────────┤
│              1 │ 2024-03-01 │ 2024-03-01 10:15:50.52  │ … │ ANON-0000-0000-0001 │         38.70 │ Latte         │
│              2 │ 2024-03-01 │ 2024-03-01 12:19:22.539 │ … │ ANON-0000-0000-0002 │         38.70 │ Hot Chocolate │
│              3 │ 2024-03-01 │ 2024-03-01 12:20:18.089 │ … │ ANON-0000-0000-0002 │         38.70 │ Hot Chocolate │
│              4 │ 2024-03-01 │ 2024-03-01 13:46:33.006 │ … │ ANON-0000-0000-0003 │         28.90 │ Americano     │
│              5 │ 2024-03-01 │ 2024-03-01 13:48:14.626 │ … │ ANON-0000-0000-0004 │         38.70 │ Latte         │
└────────────────┴────────────┴─────────────────────────┴───┴─────────────────────┴───────────────┴───────────────┘
  5 rows                                                                                      7 columns (6 shown)
*/

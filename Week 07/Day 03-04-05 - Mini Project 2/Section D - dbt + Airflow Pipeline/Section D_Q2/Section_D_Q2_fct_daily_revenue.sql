-- ============================================================================
-- BrewBeats — Mini Project 2: Section D (dbt + Airflow Pipeline)
-- Folder: Section D - dbt + Airflow Pipeline/Section D_Q2/
-- File  : Section_D_Q2_fct_daily_revenue.sql (and models/marts/fct_daily_revenue.sql)
-- Task  : Section D - Q2: Create a mart model that calculates total daily revenue.
-- ============================================================================
-- What is a mart model in dbt and how does this query work?
-- A mart model (fct_daily_revenue) is our final business-ready table (materialized as a physical 'table')
-- that dashboards and analysts query directly:
-- 1. {{ config(materialized='table') }}: tells dbt to build this model as a physical table in our warehouse.
-- 2. WITH staging AS (...): reads from our cleaned staging model using dbt's {{ ref('stg_coffee_sales') }}
--    function (which automatically tells dbt that stg_coffee_sales must run before fct_daily_revenue!).
-- 3. GROUP BY sale_date: groups all transactions by calendar day so we get 1 summary row per day:
--      * COUNT(transaction_id) AS total_transactions: total cups of coffee sold that day.
--      * ROUND(SUM(amount), 2) AS total_daily_revenue: total money earned that day, rounded to 2 decimals.
--      * ROUND(AVG(amount), 2) AS avg_transaction_value: average spend per transaction on that day.
--      * ROUND(SUM(CASE WHEN payment_type = 'card' THEN amount ELSE 0 END), 2) AS card_revenue: daily card revenue.
--      * ROUND(SUM(CASE WHEN payment_type = 'cash' THEN amount ELSE 0 END), 2) AS cash_revenue: daily cash revenue.
-- 4. ORDER BY sale_date ASC: orders our daily revenue table chronologically.

{{ config(materialized='table') }}

with staging as (

    select * from {{ ref('stg_coffee_sales') }}

),

daily_revenue as (

    select
        sale_date,
        count(transaction_id) as total_transactions,
        round(sum(amount), 2) as total_daily_revenue,
        round(avg(amount), 2) as avg_transaction_value,
        round(sum(case when payment_type = 'card' then amount else 0 end), 2) as card_revenue,
        round(sum(case when payment_type = 'cash' then amount else 0 end), 2) as cash_revenue
    from staging
    group by sale_date
    order by sale_date asc

)

select * from daily_revenue

/*
Verified Sample Output (Top 5 Days from fct_daily_revenue):
+------------+--------------------+---------------------+-----------------------+--------------+--------------+
| SALE_DATE  | TOTAL_TRANSACTIONS | TOTAL_DAILY_REVENUE | AVG_TRANSACTION_VALUE | CARD_REVENUE | CASH_REVENUE |
+------------+--------------------+---------------------+-----------------------+--------------+--------------+
| 2024-03-01 |                 11 |              396.30 |                 36.03 |       396.30 |         0.00 |
| 2024-03-02 |                  7 |              228.10 |                 32.59 |       188.10 |        40.00 |
| 2024-03-03 |                 10 |              349.10 |                 34.91 |       309.10 |        40.00 |
| 2024-03-04 |                  4 |              135.20 |                 33.80 |       135.20 |         0.00 |
| 2024-03-05 |                  9 |              338.50 |                 37.61 |       338.50 |         0.00 |
+------------+--------------------+---------------------+-----------------------+--------------+--------------+
*/

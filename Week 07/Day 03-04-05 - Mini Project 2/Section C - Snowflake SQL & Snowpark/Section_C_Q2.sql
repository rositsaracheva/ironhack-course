-- ============================================================================
-- BrewBeats — Mini Project 2: Section C (Snowflake SQL & Snowpark)
-- File  : Section_C_Q2.sql
-- Folder: Section C - Snowflake SQL & Snowpark/
-- Table : brewbeats_db.sales.coffee_sales
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Section C - Q2: Write a query to find the top 3 coffee types by revenue.
-- ----------------------------------------------------------------------------
-- How I calculate this in Snowflake SQL:
-- 1. USE WAREHOUSE / DATABASE / SCHEMA: sets our active Snowflake context to brewbeats_db.sales.
-- 2. SELECT coffee_name: picks the name of each coffee drink.
-- 3. COUNT(*) AS total_transactions: counts how many cups were sold for each coffee type.
-- 4. ROUND(SUM(money), 2) AS total_revenue: adds up all the money earned for that coffee type
--    and rounds it to 2 decimal places (cents).
-- 5. FROM coffee_sales: reads from our Snowflake coffee_sales table (loaded in Section C - Q1).
-- 6. GROUP BY coffee_name: groups all transactions by coffee name so we get 1 total row per drink.
-- 7. ORDER BY total_revenue DESC: orders the drinks from highest revenue to lowest revenue.
-- 8. LIMIT 3: keeps only the top 3 coffee types by revenue.

USE WAREHOUSE brewbeats_wh;
USE DATABASE brewbeats_db;
USE SCHEMA brewbeats_db.sales;

SELECT
    coffee_name,
    COUNT(*) AS total_transactions,
    ROUND(SUM(money), 2) AS total_revenue
FROM coffee_sales
GROUP BY coffee_name
ORDER BY total_revenue DESC
LIMIT 3;

/*
Verified Output (Section C - Q2):
+-------------------+------------------+-------------+
| COFFEE_NAME       | TOTAL_TRANSACTIONS| TOTAL_REVENUE|
+-------------------+------------------+-------------+
| Latte             |              782 |     27866.30|
| Americano with Milk|             824 |     25269.12|
| Cappuccino        |              501 |     18034.14|
+-------------------+------------------+-------------+
*/

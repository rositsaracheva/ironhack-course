-- ============================================================================
-- BrewBeats — Mini Project 2: Section B (SQL on DatabricksSQL)
-- File  : Section_B_Q2.sql
-- Folder: Section B - SQL on DatabricksSQL/
-- Table : coffee_sales (date, datetime, cash_type, card, money, coffee_name)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Section B - Q2: Write a query to find total revenue by payment type (cash_type).
-- ----------------------------------------------------------------------------
-- How I calculate this:
-- 1. SELECT cash_type: picks the payment method column ('card' or 'cash').
-- 2. COUNT(*) AS total_transactions: counts how many sales were paid with each payment method.
-- 3. ROUND(SUM(money), 2) AS total_revenue: adds up all money spent for each payment method,
--    rounded to 2 decimal places (cents).
-- 4. ROUND(AVG(money), 2) AS avg_transaction_value: calculates the average amount spent per
--    transaction for each payment method.
-- 5. FROM coffee_sales: reads from our coffee_sales table in Databricks.
-- 6. GROUP BY cash_type: groups all rows by payment type ('card' vs 'cash') so the totals are
--    calculated separately for each payment method.
-- 7. ORDER BY total_revenue DESC: orders the result from highest revenue to lowest revenue.

SELECT
    cash_type,
    COUNT(*) AS total_transactions,
    ROUND(SUM(money), 2) AS total_revenue,
    ROUND(AVG(money), 2) AS avg_transaction_value
FROM coffee_sales
GROUP BY cash_type
ORDER BY total_revenue DESC;

/*
Verified Output (Section B - Q2):
+---------+------------------+-------------+---------------------+
|cash_type|total_transactions|total_revenue|avg_transaction_value|
+---------+------------------+-------------+---------------------+
|     card|              3547|    112245.58|                31.65|
|     cash|                89|       3186.0|                 35.8|
+---------+------------------+-------------+---------------------+
*/

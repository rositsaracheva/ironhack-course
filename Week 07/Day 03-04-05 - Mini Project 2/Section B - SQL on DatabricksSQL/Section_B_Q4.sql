-- ============================================================================
-- BrewBeats — Mini Project 2: Section B (SQL on DatabricksSQL)
-- File  : Section_B_Q4.sql
-- Folder: Section B - SQL on DatabricksSQL/
-- Table : coffee_sales (date, datetime, cash_type, card, money, coffee_name)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Section B - Q4: Write a query to find the day with the highest number of transactions.
-- ----------------------------------------------------------------------------
-- How I calculate this:
-- 1. SELECT date: picks the calendar date of the transactions (e.g., '2024-10-11').
-- 2. DATE_FORMAT(date, 'EEEE') AS day_of_week: extracts the weekday name (e.g., 'Friday')
--    so we can also see which day of the week was the busiest.
-- 3. COUNT(*) AS total_transactions: counts how many coffee transactions happened on that date.
-- 4. ROUND(SUM(money), 2) AS daily_revenue: adds up the total revenue earned on that date.
-- 5. FROM coffee_sales: reads from our coffee_sales table in Databricks.
-- 6. GROUP BY date: groups all sales by calendar date so COUNT(*) and SUM(money) are calculated per day.
-- 7. ORDER BY total_transactions DESC, daily_revenue DESC: sorts from the busiest day to the quietest day.
-- 8. LIMIT 1: returns the single day with the highest number of transactions.

SELECT
    date,
    DATE_FORMAT(date, 'EEEE') AS day_of_week,
    COUNT(*) AS total_transactions,
    ROUND(SUM(money), 2) AS daily_revenue
FROM coffee_sales
GROUP BY date
ORDER BY total_transactions DESC, daily_revenue DESC
LIMIT 1;

/*
Verified Output (Section B - Q4):
+----------+-----------+------------------+-------------+
|      date|day_of_week|total_transactions|daily_revenue|
+----------+-----------+------------------+-------------+
|2024-10-11|     Friday|                26|       836.66|
+----------+-----------+------------------+-------------+

Top 5 Busiest Days (Context):
+----------+-----------+------------------+-------------+
|      date|day_of_week|total_transactions|daily_revenue|
+----------+-----------+------------------+-------------+
|2024-10-11|     Friday|                26|       836.66|
|2025-02-03|     Monday|                25|        796.0|
|2025-02-05|  Wednesday|                24|       760.24|
|2024-09-22|     Sunday|                24|       679.88|
|2024-07-30|    Tuesday|                24|       650.48|
+----------+-----------+------------------+-------------+
*/

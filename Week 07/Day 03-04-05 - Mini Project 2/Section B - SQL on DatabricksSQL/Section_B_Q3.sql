-- ============================================================================
-- BrewBeats — Mini Project 2: Section B (SQL on DatabricksSQL)
-- File  : Section_B_Q3.sql
-- Folder: Section B - SQL on DatabricksSQL/
-- Table : coffee_sales (date, datetime, cash_type, card, money, coffee_name)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Section B - Q3: Write a query using a CTE to find total revenue per month.
-- ----------------------------------------------------------------------------
-- How I calculate this:
-- 1. WITH monthly_sales AS (...): creates a CTE (Common Table Expression) — a temporary named
--    result set that prepares our month columns from the 'date' column before we group them:
--      * DATE_FORMAT(date, 'yyyy-MM') AS year_month: extracts Year and Month (e.g., '2024-03')
--        so March 2024 and March 2025 stay separate.
--      * MONTH(date) AS month_number: extracts the month number (1 to 12).
--      * DATE_FORMAT(date, 'MMMM') AS month_name: extracts the full month name (e.g., 'March').
-- 2. Main SELECT ... FROM monthly_sales: queries our CTE table:
--      * COUNT(*) AS total_transactions: counts how many coffee sales occurred in each month.
--      * ROUND(SUM(money), 2) AS monthly_revenue: adds up the total revenue for each month,
--        rounded to 2 decimal places.
-- 3. GROUP BY year_month, month_number, month_name: groups all transactions by month.
-- 4. ORDER BY year_month ASC: sorts the months chronologically from earliest to latest.

WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(date, 'yyyy-MM') AS year_month,
        MONTH(date) AS month_number,
        DATE_FORMAT(date, 'MMMM') AS month_name,
        money
    FROM coffee_sales
)
SELECT
    year_month,
    month_number,
    month_name,
    COUNT(*) AS total_transactions,
    ROUND(SUM(money), 2) AS monthly_revenue
FROM monthly_sales
GROUP BY year_month, month_number, month_name
ORDER BY year_month ASC;

/*
Verified Output (Section B - Q3):
+----------+------------+----------+------------------+---------------+
|year_month|month_number|month_name|total_transactions|monthly_revenue|
+----------+------------+----------+------------------+---------------+
|   2024-03|           3|     March|               206|         7050.2|
|   2024-04|           4|     April|               196|        6720.56|
|   2024-05|           5|       May|               267|        9063.42|
|   2024-06|           6|      June|               227|        7758.76|
|   2024-07|           7|      July|               237|        6915.94|
|   2024-08|           8|    August|               272|        7613.84|
|   2024-09|           9| September|               344|        9988.64|
|   2024-10|          10|   October|               426|       13891.16|
|   2024-11|          11|  November|               259|        8590.54|
|   2024-12|          12|  December|               259|        8237.74|
|   2025-01|           1|   January|               201|        6398.86|
|   2025-02|           2|  February|               423|       13215.48|
|   2025-03|           3|     March|               319|        9986.44|
+----------+------------+----------+------------------+---------------+
*/

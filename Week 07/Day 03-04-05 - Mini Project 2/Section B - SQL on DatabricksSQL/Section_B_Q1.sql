-- ============================================================================
-- BrewBeats — Mini Project 2: Section B (SQL on DatabricksSQL)
-- Folder: Section B - SQL on DatabricksSQL/
-- Table : coffee_sales (date, datetime, cash_type, card, money, coffee_name)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Section B - Q1: Write a query to find the top 5 best-selling coffee types by revenue.
-- ----------------------------------------------------------------------------
-- How I calculate this:
-- 1. SELECT coffee_name: picks the name of each coffee drink.
-- 2. COUNT(*) AS total_transactions: counts how many cups were sold for each coffee type.
-- 3. ROUND(SUM(money), 2) AS total_revenue: adds up all the sales ('money') for that coffee
--    and rounds it to 2 decimal places (cents).
-- 4. FROM coffee_sales: reads from our coffee_sales table in Databricks.
-- 5. GROUP BY coffee_name: groups all rows with the same coffee name into one summary row.
-- 6. ORDER BY total_revenue DESC: sorts the coffees from highest revenue to lowest revenue.
-- 7. LIMIT 5: keeps only the top 5 best-selling coffee types.

SELECT
    coffee_name,
    COUNT(*) AS total_transactions,
    ROUND(SUM(money), 2) AS total_revenue
FROM coffee_sales
GROUP BY coffee_name
ORDER BY total_revenue DESC
LIMIT 5;

/*
Verified Output (Section B - Q1):
+-------------------+------------------+-------------+
|        coffee_name|total_transactions|total_revenue|
+-------------------+------------------+-------------+
|              Latte|               782|      27866.3|
|Americano with Milk|               824|     25269.12|
|         Cappuccino|               501|     18034.14|
|          Americano|               578|     15062.26|
|      Hot Chocolate|               282|     10172.46|
+-------------------+------------------+-------------+
*/

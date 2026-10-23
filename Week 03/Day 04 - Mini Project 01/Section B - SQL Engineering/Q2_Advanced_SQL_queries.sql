-- =====================================================================
-- SECTION B: SQL ENGINEERING
-- Q2. Advanced SQL Queries (Window Functions)
-- Platform: QuickCart E-Commerce
-- Database: quickcart.db
-- =====================================================================

-- ---------------------------------------------------------------------
-- Task 1: Rank Customers Based on Total Revenue
-- Description:
-- Uses DENSE_RANK() OVER (ORDER BY total_revenue DESC) to assign a ranking
-- to each customer based on their total paid order value.
-- ---------------------------------------------------------------------
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    DENSE_RANK() OVER (ORDER BY SUM(o.quantity * o.unit_price) DESC) AS revenue_rank
FROM customers c
JOIN orders o 
    ON c.customer_id = o.customer_id
WHERE o.payment_status = 'Paid'
GROUP BY 
    c.customer_id, 
    c.customer_name, 
    c.city
ORDER BY revenue_rank ASC
LIMIT 10;

/*
=== OUTPUT (Task 1 - Top 10 Ranked Customers) ===
customer_id | customer_name           | city       | total_revenue | revenue_rank
------------+-------------------------+------------+---------------+-------------
95          | Miss Olivia Taylor      | Brussels   | 42015.00      | 1
90          | Mr Russell Jennings     | Manchester | 28484.00      | 2
64          | Mrs Jessica Jackson     | Rome       | 27782.00      | 3
65          | Mr Matthew Hunt         | Manchester | 27629.00      | 4
74          | Mrs Lesley Charlton     | Warsaw     | 27622.00      | 5
86          | Liam Sykes              | Manchester | 26698.00      | 6
98          | Louise Jackson-Robinson | Paris      | 24281.00      | 7
23          | Bernard Wilkins         | Rome       | 24091.00      | 8
91          | Dr Hollie Taylor        | Berlin     | 24042.00      | 9
12          | Sean Norton             | Lisbon     | 21250.00      | 10
*/


-- ---------------------------------------------------------------------
-- Task 2: Find Running Total Sales by Month
-- Description:
-- Groups sales by month, then uses SUM() OVER (ORDER BY month) to compute
-- a cumulative running revenue balance over time.
-- ---------------------------------------------------------------------
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', order_date) AS sales_month,
        ROUND(SUM(quantity * unit_price), 2) AS month_sales
    FROM orders
    WHERE payment_status = 'Paid'
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT 
    sales_month,
    month_sales,
    ROUND(
        SUM(month_sales) OVER (
            ORDER BY sales_month 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ), 
        2
    ) AS running_total_revenue
FROM monthly_sales
ORDER BY sales_month
LIMIT 10;

/*
=== OUTPUT (Task 2 - Sample Running Total) ===
sales_month | month_sales | running_total_revenue
------------+-------------+----------------------
2024-09     | 10694.00    | 10694.00
2024-10     | 10794.00    | 21488.00
2024-11     | 3998.00     | 25486.00
2024-12     | 745.00      | 26231.00
2025-01     | 15843.00    | 42074.00
2025-02     | 12238.00    | 54312.00
2025-03     | 7952.00     | 62264.00
2025-04     | 8136.00     | 70400.00
2025-05     | 26485.00    | 96885.00
2025-06     | 8410.00     | 105295.00
...
*/


-- ---------------------------------------------------------------------
-- Task 3: Find the Highest Selling Product Per Category
-- Description:
-- Partitions by product category, orders by total revenue descending,
-- and uses ROW_NUMBER() to identify the #1 top-selling item per category.
-- ---------------------------------------------------------------------
WITH product_revenue_per_category AS (
    SELECT 
        p.category,
        p.product_id,
        p.product_name,
        SUM(o.quantity) AS total_units_sold,
        ROUND(SUM(o.quantity * o.unit_price), 2) AS total_product_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY p.category 
            ORDER BY SUM(o.quantity * o.unit_price) DESC
        ) AS rank_in_category
    FROM products p
    JOIN orders o 
        ON p.product_id = o.product_id
    WHERE o.payment_status = 'Paid'
    GROUP BY 
        p.category, 
        p.product_id, 
        p.product_name
)
SELECT 
    category,
    product_id,
    product_name,
    total_units_sold,
    total_product_revenue
FROM product_revenue_per_category
WHERE rank_in_category = 1
ORDER BY total_product_revenue DESC;

/*
=== OUTPUT (Task 3 - Highest Selling Product Per Category) ===
category      | product_id | product_name         | total_units_sold | total_product_revenue
--------------+------------+----------------------+------------------+----------------------
Electronics   | 105        | 4K Monitor           | 147              | 293853.00
Furniture     | 109        | Standing Desk        | 110              | 274890.00
Accessories   | 110        | Backpack             | 145              | 72355.00
Home & Living | 108        | Water Bottle         | 115              | 17135.00
Stationery    | 104        | Notebook Pack        | 125              | 11125.00
*/


-- ---------------------------------------------------------------------
-- Task 4: Find 7-Day Rolling Average Sales
-- Description:
-- Aggregates daily sales, then applies AVG() over a sliding frame of 
-- 6 preceding days + current day (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW).
-- ---------------------------------------------------------------------
WITH daily_sales AS (
    SELECT 
        date(order_date) AS sales_date,
        ROUND(SUM(quantity * unit_price), 2) AS daily_revenue
    FROM orders
    WHERE payment_status = 'Paid'
    GROUP BY date(order_date)
)
SELECT 
    sales_date,
    daily_revenue,
    ROUND(
        AVG(daily_revenue) OVER (
            ORDER BY sales_date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 
        2
    ) AS rolling_7day_avg_revenue
FROM daily_sales
ORDER BY sales_date
LIMIT 12;

/*
=== OUTPUT (Task 4 - Sample 7-Day Rolling Average) ===
sales_date | daily_revenue | rolling_7day_avg_revenue
-----------+---------------+-------------------------
2024-09-26 | 698.00        | 698.00
2024-09-30 | 9996.00       | 5347.00
2024-10-06 | 9995.00       | 6896.33
2024-10-15 | 799.00        | 5372.00
2024-11-05 | 3998.00       | 5097.20
2024-12-13 | 745.00        | 4371.83
2025-01-04 | 356.00        | 3798.14
2025-01-10 | 747.00        | 3805.14
2025-01-12 | 6495.00       | 3305.00
2025-01-15 | 7996.00       | 3019.43
2025-01-17 | 249.00        | 2940.86
2025-02-07 | 599.00        | 2455.29
...
*/

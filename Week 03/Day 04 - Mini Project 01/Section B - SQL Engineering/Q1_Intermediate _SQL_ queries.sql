-- =====================================================================
-- SECTION B: SQL ENGINEERING
-- Q1. Intermediate SQL Queries
-- Platform: QuickCart E-Commerce
-- Database: quickcart.db
-- =====================================================================

-- ---------------------------------------------------------------------
-- Task 1: Find Top 10 Customers by Revenue
-- Description:
-- Joins customers with orders, filters for 'Paid' orders, calculates
-- total revenue (quantity * unit_price), and ranks the top 10.
-- ---------------------------------------------------------------------
SELECT 
    c.customer_id,
    c.customer_name,
    c.email,
    c.city,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue
FROM customers c
JOIN orders o 
    ON c.customer_id = o.customer_id
WHERE o.payment_status = 'Paid'
GROUP BY 
    c.customer_id, 
    c.customer_name, 
    c.email, 
    c.city
ORDER BY total_revenue DESC
LIMIT 10;

/*
=== OUTPUT (Task 1) ===
customer_id | customer_name           | email                             | city       | total_revenue
------------+-------------------------+-----------------------------------+------------+--------------
95          | Miss Olivia Taylor      | miss.olivia.taylor95@example.com  | Brussels   | 42015.00
90          | Mr Russell Jennings     | mr.russell.jennings90@example.com | Manchester | 28484.00
64          | Mrs Jessica Jackson     | mrs.jessica.jackson64@example.com | Rome       | 27782.00
65          | Mr Matthew Hunt         | mr.matthew.hunt65@example.com     | Manchester | 27629.00
74          | Mrs Lesley Charlton     | mrs.lesley.charlton74@example.com | Warsaw     | 27622.00
86          | Liam Sykes              | liam.sykes86@example.com          | Manchester | 26698.00
98          | Louise Jackson-Robinson | louise.jackson-robinson98@example | Paris      | 24281.00
23          | Bernard Wilkins         | bernard.wilkins23@example.com     | Rome       | 24091.00
91          | Dr Hollie Taylor        | dr.hollie.taylor91@example.com    | Berlin     | 24042.00
12          | Sean Norton             | sean.norton12@example.com         | Lisbon     | 21250.00
*/


-- ---------------------------------------------------------------------
-- Task 2: Find Month-over-Month (MoM) Sales Growth
-- Description:
-- Aggregates monthly revenue using strftime, then applies the LAG() 
-- window function to compute percentage revenue change vs previous month.
-- ---------------------------------------------------------------------
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', order_date) AS sales_month,
        ROUND(SUM(quantity * unit_price), 2) AS current_month_revenue
    FROM orders
    WHERE payment_status = 'Paid'
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT 
    sales_month,
    current_month_revenue,
    LAG(current_month_revenue, 1) OVER (ORDER BY sales_month) AS previous_month_revenue,
    ROUND(
        ((current_month_revenue - LAG(current_month_revenue, 1) OVER (ORDER BY sales_month)) 
        / LAG(current_month_revenue, 1) OVER (ORDER BY sales_month)) * 100.0, 
        2
    ) AS mom_growth_percentage
FROM monthly_sales
ORDER BY sales_month;

/*
=== OUTPUT (Task 2 - Sample First 10 Months) ===
sales_month | current_month_revenue | previous_month_revenue | mom_growth_percentage
------------+-----------------------+------------------------+----------------------
2024-09     | 10694.00              | NULL                   | NULL
2024-10     | 10794.00              | 10694.00               | 0.94%
2024-11     | 3998.00               | 10794.00               | -62.96%
2024-12     | 745.00                | 3998.00                | -81.37%
2025-01     | 15843.00              | 745.00                 | 2026.58%
2025-02     | 12238.00              | 15843.00               | -22.75%
2025-03     | 7952.00               | 12238.00               | -35.02%
2025-04     | 8136.00               | 7952.00                | 2.31%
2025-05     | 26485.00              | 8136.00                | 225.53%
2025-06     | 8410.00               | 26485.00               | -68.25%
...
*/


-- ---------------------------------------------------------------------
-- Task 3: Find Customers Who Ordered in Consecutive Months
-- Description:
-- Maps each order date to an integer month index (Year * 12 + Month).
-- Uses LAG() per customer to detect an exact 1-month difference.
-- ---------------------------------------------------------------------
WITH customer_order_months AS (
    SELECT DISTINCT
        customer_id,
        CAST(strftime('%Y', order_date) AS INT) * 12 + CAST(strftime('%m', order_date) AS INT) AS month_index
    FROM orders
    WHERE payment_status = 'Paid'
),
month_intervals AS (
    SELECT 
        customer_id,
        month_index,
        LAG(month_index, 1) OVER (PARTITION BY customer_id ORDER BY month_index) AS prev_month_index
    FROM customer_order_months
)
SELECT DISTINCT 
    c.customer_id,
    c.customer_name,
    c.email,
    c.city
FROM month_intervals mi
JOIN customers c 
    ON mi.customer_id = c.customer_id
WHERE mi.month_index - mi.prev_month_index = 1
ORDER BY c.customer_id;

/*
=== OUTPUT (Task 3 - Sample Top 10 of 39 Consecutive Customers) ===
customer_id | customer_name         | email                             | city
------------+-----------------------+-----------------------------------+------------
1           | William Jennings      | william.jennings1@example.com     | Dublin
4           | Gillian Barnes        | gillian.barnes4@example.com       | Lisbon
8           | Gillian Andrews       | gillian.andrews8@example.com      | Birmingham
9           | Janice Glover         | janice.glover9@example.com        | Lisbon
10          | Wayne Gough           | wayne.gough10@example.com         | Manchester
12          | Sean Norton           | sean.norton12@example.com         | Lisbon
16          | Dr Jonathan Middleton | dr.jonathan.middleton16@example.c | Amsterdam
17          | Diana Cross-Miah      | diana.cross-miah17@example.com    | Berlin
19          | Miss Frances Holmes   | miss.frances.holmes19@example.com | London
21          | Miss Charlotte Kelly  | miss.charlotte.kelly21@example.co | Edinburgh
Total Consecutive Customers: 39
*/


-- ---------------------------------------------------------------------
-- Task 4: Find Products Never Ordered
-- Description:
-- Performs a LEFT JOIN from products to orders; products with no matching 
-- orders will have a NULL order_id.
-- ---------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.cost_price,
    p.selling_price
FROM products p
LEFT JOIN orders o 
    ON p.product_id = o.product_id
WHERE o.order_id IS NULL;

/*
=== OUTPUT (Task 4) ===
product_id | product_name | category | cost_price | selling_price
-----------+--------------+----------+------------+--------------
(0 rows returned)
Note: All 10 products in QuickCart's product catalogue have at least 1 order recorded.
*/


-- ---------------------------------------------------------------------
-- Task 5: Find Revenue Contribution Percentage by Category
-- Description:
-- Calculates total revenue per product category, then uses an OVER () 
-- window function to compute each category's percentage of total company revenue.
-- ---------------------------------------------------------------------
WITH category_sales AS (
    SELECT 
        p.category,
        ROUND(SUM(o.quantity * o.unit_price), 2) AS category_revenue
    FROM orders o
    JOIN products p 
        ON o.product_id = p.product_id
    WHERE o.payment_status = 'Paid'
    GROUP BY p.category
)
SELECT 
    category,
    category_revenue,
    ROUND(
        (category_revenue * 100.0) / SUM(category_revenue) OVER (), 
        2
    ) AS revenue_contribution_pct
FROM category_sales
ORDER BY category_revenue DESC;

/*
=== OUTPUT (Task 5) ===
category      | category_revenue | revenue_contribution_pct
--------------+------------------+-------------------------
Furniture     | 466,504.00       | 45.97%
Electronics   | 447,724.00       | 44.12%
Accessories   | 72,355.00        | 7.13%
Home & Living | 17,135.00        | 1.69%
Stationery    | 11,125.00        | 1.10%
Total Revenue : 1,014,843.00     | 100.00%
*/

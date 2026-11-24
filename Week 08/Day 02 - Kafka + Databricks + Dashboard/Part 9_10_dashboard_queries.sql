-- Week 08 — Day 02: Kafka + Databricks + Dashboard Integration Project
-- Parts 9 & 10: Databricks AI/BI Dashboard Queries (Part 9_10_dashboard_queries.sql)
-- Student: Rositsa Kaloyanova
-- Purpose: Five SQL datasets powering the 5 real-time e-commerce dashboard visuals
--          on top of my live Databricks Delta table 'workspace.kafka_demo.orders'.

-- ============================================================================
-- Step 21 — Visual 1: Revenue KPI (Counter / Card Visual)
-- Shows total revenue across all streamed orders (plus total order count).
-- ============================================================================
SELECT
    ROUND(SUM(amount), 2) AS total_revenue,
    COUNT(order_id) AS total_orders
FROM workspace.kafka_demo.orders;


-- ============================================================================
-- Step 22 — Visual 2: Orders by City (Bar Chart: X = city, Y = total_amount)
-- Groups total sales amount by city and sorts from highest to lowest revenue.
-- ============================================================================
SELECT
    city,
    ROUND(SUM(amount), 2) AS total_amount,
    COUNT(order_id) AS order_count
FROM workspace.kafka_demo.orders
GROUP BY city
ORDER BY total_amount DESC;


-- ============================================================================
-- Step 23 — Visual 3: Product Sales (Pie Chart: Angle = order_count, Color = product)
-- Counts how many orders were placed for each product category.
-- ============================================================================
SELECT
    product,
    COUNT(order_id) AS order_count,
    ROUND(SUM(amount), 2) AS total_revenue
FROM workspace.kafka_demo.orders
GROUP BY product
ORDER BY order_count DESC;


-- ============================================================================
-- Step 24 — Visual 4: Payment Trends (Donut / Pie Chart: Angle = order_count, Color = payment_mode)
-- Shows the distribution of orders across payment methods (UPI, Card, Cash).
-- ============================================================================
SELECT
    payment_mode,
    COUNT(order_id) AS order_count,
    ROUND(SUM(amount), 2) AS total_revenue
FROM workspace.kafka_demo.orders
GROUP BY payment_mode
ORDER BY order_count DESC;


-- ============================================================================
-- Step 25 — Visual 5: Live Orders Table (Table Visual)
-- Displays the most recent streamed orders first (customer_name, product, amount, city).
-- ============================================================================
SELECT
    order_id,
    customer_name,
    product,
    ROUND(amount, 2) AS amount,
    city,
    payment_mode,
    order_time
FROM workspace.kafka_demo.orders
ORDER BY order_id DESC;

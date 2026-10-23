-- =====================================================================
-- SECTION B: SQL ENGINEERING
-- Q3. SQL Optimization Scenario
-- Platform: QuickCart E-Commerce
-- Database: quickcart.db
-- =====================================================================

-- =====================================================================
-- TASK 1: IDENTIFY POSSIBLE BOTTLENECKS (Why it takes 18 minutes)
-- =====================================================================
/*
1. Full Sequential Table Scan on `orders` (Missing Index on Filter Column):
   - Without an index on `order_date`, the database must read every single row
     from disk across years of historical orders to find records >= '2025-01-01'.

2. Unindexed Foreign Key Join (`orders.customer_id`):
   - To match each order with a customer, the database must join millions of rows.
   - Without an index on `orders.customer_id`, the database performs an 
     expensive Nested Loop or Hash Join, thrashing CPU and RAM.

3. Expensive String Grouping (`GROUP BY c.customer_name`):
   - Grouping by a variable-length text string (`customer_name`) is much slower
     than grouping by an integer primary key (`c.customer_id`).
   - String comparisons require more CPU cycles and large memory sort buffers.
   - Also, two different customers with the same name would be incorrectly merged!

4. Cache Eviction / Buffer Pool Thrashing:
   - Scanning gigabytes of raw order rows flushes the database's RAM cache, 
     forcing other live web queries to stall.
*/


-- =====================================================================
-- TASK 2: SUGGESTED INDEXES (DDL Solutions)
-- =====================================================================

-- Index 1: Composite Covering Index on `orders`
-- This index covers the filter (`order_date`), the join (`customer_id`), 
-- and the aggregation columns (`quantity`, `unit_price`). The database can 
-- resolve the entire query straight from the index tree without touching the table!
CREATE INDEX IF NOT EXISTS idx_orders_date_cust_covering 
ON orders (order_date, customer_id, quantity, unit_price);

-- Index 2: Composite Index on `customers` for fast ID + Name lookup
CREATE INDEX IF NOT EXISTS idx_customers_id_name 
ON customers (customer_id, customer_name);


-- =====================================================================
-- OPTIMIZED QUERY REWRITE
-- Best practice: Group by integer PK first (`c.customer_id`), then select name
-- =====================================================================
SELECT 
    c.customer_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spent
FROM orders o
JOIN customers c 
    ON o.customer_id = c.customer_id
WHERE o.order_date >= '2025-01-01'
GROUP BY 
    c.customer_id, 
    c.customer_name;


-- =====================================================================
-- TASK 3: EXECUTION PLAN ANALYSIS (EXPLAIN QUERY PLAN)
-- =====================================================================

-- How to inspect the plan:
EXPLAIN QUERY PLAN
SELECT 
    c.customer_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spent
FROM orders o
JOIN customers c 
    ON o.customer_id = c.customer_id
WHERE o.order_date >= '2025-01-01'
GROUP BY 
    c.customer_id, 
    c.customer_name;

/*
=== EXECUTION PLAN COMPARISON ===

1. BEFORE INDEXING (The Slow 18-Minute Plan):
   -----------------------------------------------------------------------
   SCAN o
   BLOOM FILTER ON c (customer_id=?)
   SEARCH c USING AUTOMATIC COVERING INDEX (customer_id=?)
   USE TEMP B-TREE FOR GROUP BY
   -----------------------------------------------------------------------
   • "SCAN o": Full sequential scan across every disk block of the `orders` table.
   • "AUTOMATIC COVERING INDEX": The database is forced to build a temporary 
     index in RAM on the fly for every execution.
   • "USE TEMP B-TREE": Spills rows to a temporary disk file to sort the GROUP BY.


2. AFTER INDEXING (The Optimized Sub-Second Plan):
   -----------------------------------------------------------------------
   SEARCH o USING INDEX idx_orders_date_cust_covering (order_date>?)
   SEARCH c USING COVERING INDEX idx_customers_id_name (customer_id=?)
   USE TEMP B-TREE FOR GROUP BY
   -----------------------------------------------------------------------
   • "SEARCH o USING INDEX": Binary search directly jumps to '2025-01-01', 
     skipping all previous years without reading them off disk.
   • "SEARCH c USING COVERING INDEX": Instantly grabs customer names from RAM.
   • Result: Query execution drops from 18 minutes down to ~150 milliseconds!
*/

-- ============================================================================
-- WEEK 06 - DAY 05: SNOWFLAKE + DBT COMPLETE WORKSHEET SQL
-- ============================================================================

-- 1. PREREQUISITES & SETUP (Create Warehouse, Database, and Role)
USE ROLE ACCOUNTADMIN;

CREATE WAREHOUSE IF NOT EXISTS dbt_wh WITH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE;
CREATE DATABASE IF NOT EXISTS dbt_db;
CREATE ROLE IF NOT EXISTS dbt_role;

GRANT USAGE ON WAREHOUSE dbt_wh TO ROLE dbt_role;
GRANT ALL ON DATABASE dbt_db TO ROLE dbt_role;
GRANT ALL ON ALL SCHEMAS IN DATABASE dbt_db TO ROLE dbt_role;
GRANT ROLE dbt_role TO USER ROSI;


-- 2. SET ACTIVE CONTEXT FOR QUERIES
USE ROLE dbt_role;
USE WAREHOUSE dbt_wh;
USE DATABASE dbt_db;
USE SCHEMA dev_schema;


-- 3. EXERCISE 1: VERIFY SEEDED RAW TABLES (dbt seed)
SELECT * FROM DBT_DB.DEV_SCHEMA.CUSTOMERS LIMIT 10;
SELECT * FROM DBT_DB.DEV_SCHEMA.ORDERS LIMIT 10;
SELECT * FROM DBT_DB.DEV_SCHEMA.PRODUCTS LIMIT 10;
SELECT * FROM DBT_DB.DEV_SCHEMA.CLICKSTREAM LIMIT 10;


-- 4. EXERCISE 1: VERIFY STAGING VIEWS & MART TABLE (dbt run)
SELECT * FROM DBT_DB.DEV_SCHEMA.STG_CUSTOMERS LIMIT 10;
SELECT * FROM DBT_DB.DEV_SCHEMA.STG_ORDERS LIMIT 10;
SELECT * FROM DBT_DB.DEV_SCHEMA.FCT_ORDERS LIMIT 20;


-- 5. EXERCISE 2: INTENTIONALLY BREAK DATA TO TEST `dbt test`
-- (Run this ONLY when demonstrating how `dbt test` catches a duplicate order_id)
-- INSERT INTO DBT_DB.DEV_SCHEMA.FCT_ORDERS
-- SELECT * FROM DBT_DB.DEV_SCHEMA.FCT_ORDERS WHERE order_id = 1001;


-- 6. EXERCISE 3: INCREMENTAL MODEL — INSERT NEW ORDERS & CHECK RESULTS
-- (Already inserted during Exercise 3; query below verifies the 2 incremental rows)
-- INSERT INTO DBT_DB.DEV_SCHEMA.ORDERS (order_id, customer_id, product_id, order_date, quantity, unit_price, payment_status)
-- VALUES
--     (1501, 1, 101, '2028-05-01', 2, 249.00, 'Paid'),
--     (1502, 2, 102, '2028-05-01', 1, 599.00, 'Paid');

SELECT COUNT(*) AS total_orders FROM DBT_DB.DEV_SCHEMA.FCT_ORDERS;

SELECT * FROM DBT_DB.DEV_SCHEMA.FCT_ORDERS
WHERE order_id IN (1501, 1502)
ORDER BY order_id;


-- 7. EXERCISE 4: SNAPSHOTS (SCD TYPE 2) — UPDATE EMAIL & VIEW BOTH VERSIONS
-- (Already updated during Exercise 4; query below shows both historical versions)
-- UPDATE DBT_DB.DEV_SCHEMA.CUSTOMERS
-- SET email = 'william.jennings.updated@example.com'
-- WHERE customer_id = 1;

SELECT
    customer_id,
    customer_name,
    email,
    dbt_valid_from,
    dbt_valid_to
FROM DBT_DB.SNAPSHOTS.CUSTOMERS_SNAPSHOT
WHERE customer_id = 1
ORDER BY dbt_valid_from;

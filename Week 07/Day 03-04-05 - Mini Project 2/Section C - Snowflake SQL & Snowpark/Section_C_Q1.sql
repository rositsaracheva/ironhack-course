-- ============================================================================
-- BrewBeats — Mini Project 2: Section C (Snowflake SQL & Snowpark)
-- File  : Section_C_Q1.sql
-- Folder: Section C - Snowflake SQL & Snowpark/
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Section C - Q1: Write the SQL to create a stage and load coffee_sales.csv into a Snowflake table.
-- ----------------------------------------------------------------------------
-- How I do this step by step in Snowflake:
-- 1. Create the Database (brewbeats_db), Schema (sales), and virtual Warehouse (brewbeats_wh),
--    and set them as our active context with USE.
-- 2. CREATE OR REPLACE FILE FORMAT coffee_csv_ff: defines how Snowflake should read our CSV file
--    (TYPE = CSV, SKIP_HEADER = 1 skips the first row of column names, and FIELD_OPTIONALLY_ENCLOSED_BY = '"'
--    handles quoted text).
-- 3. CREATE OR REPLACE TABLE coffee_sales: creates the destination table in Snowflake with the exact
--    6 columns and data types matching coffee_sales.csv (date, datetime, cash_type, card, money, coffee_name).
-- 4. CREATE OR REPLACE STAGE coffee_stage: creates an internal Snowflake stage (a cloud storage landing zone
--    inside Snowflake where we upload coffee_sales.csv before loading it into the table).
-- 5. COPY INTO coffee_sales FROM @coffee_stage: bulk-loads the CSV data from the stage (@coffee_stage)
--    into our coffee_sales table.

-- Step 1: Set up Database, Schema, and Warehouse
CREATE DATABASE IF NOT EXISTS brewbeats_db;
CREATE SCHEMA IF NOT EXISTS brewbeats_db.sales;
CREATE WAREHOUSE IF NOT EXISTS brewbeats_wh
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

USE WAREHOUSE brewbeats_wh;
USE DATABASE brewbeats_db;
USE SCHEMA brewbeats_db.sales;

-- Step 2: Create the CSV File Format
CREATE OR REPLACE FILE FORMAT coffee_csv_ff
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('', 'NULL');

-- Step 3: Create the target Snowflake table matching coffee_sales.csv (6 columns)
CREATE OR REPLACE TABLE coffee_sales (
    date DATE,
    datetime TIMESTAMP_NTZ,
    cash_type STRING,
    card STRING,
    money FLOAT,
    coffee_name STRING
);

-- Step 4: Create the Internal Stage using our CSV File Format
-- (After creating the stage, we upload coffee_sales.csv to @coffee_stage via Snowsight UI or PUT file://coffee_sales.csv @coffee_stage)
CREATE OR REPLACE STAGE coffee_stage
    FILE_FORMAT = coffee_csv_ff;

-- Step 5: Load coffee_sales.csv from the stage into the coffee_sales table
COPY INTO coffee_sales
FROM @coffee_stage/coffee_sales.csv
FILE_FORMAT = (FORMAT_NAME = 'coffee_csv_ff')
ON_ERROR = 'CONTINUE';

-- Step 6: Verify the loaded data (3,636 rows)
SELECT COUNT(*) AS total_rows_loaded FROM coffee_sales;
SELECT * FROM coffee_sales LIMIT 5;

/*
Verified Output (Section C - Q1):
Total Rows Loaded: 3636
+----------+-----------------------+---------+-------------------+-----+-------------+
|      date|               datetime|cash_type|               card|money|  coffee_name|
+----------+-----------------------+---------+-------------------+-----+-------------+
|2024-03-01| 2024-03-01 10:15:50.52|     card|ANON-0000-0000-0001| 38.7|        Latte|
|2024-03-01|2024-03-01 12:19:22.539|     card|ANON-0000-0000-0002| 38.7|Hot Chocolate|
|2024-03-01|2024-03-01 12:20:18.089|     card|ANON-0000-0000-0002| 38.7|Hot Chocolate|
|2024-03-01|2024-03-01 13:46:33.006|     card|ANON-0000-0000-0003| 28.9|    Americano|
|2024-03-01|2024-03-01 13:48:14.626|     card|ANON-0000-0000-0004| 38.7|        Latte|
+----------+-----------------------+---------+-------------------+-----+-------------+
*/

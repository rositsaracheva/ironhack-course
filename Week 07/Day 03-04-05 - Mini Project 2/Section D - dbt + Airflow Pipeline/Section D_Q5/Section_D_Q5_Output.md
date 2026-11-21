# Section D - Q5: Verified Airflow DAG Output (`check_mart_has_data_for_today`)

## DAG Configuration Summary
- **DAG ID:** `brewbeats_daily_dbt_pipeline_with_check`
- **Schedule:** `@daily` (runs once a day)
- **Task Flow:** `dbt_run_models >> dbt_test_models >> check_mart_has_data_for_today`

## Verified Execution Log
```text
11:57:38  Running with dbt=1.13.0-b1
11:57:38  Registered adapter: duckdb=1.11.1
11:57:38  Found 2 models, 9 data tests, 1 source, 511 macros
11:57:38  
11:57:38  Concurrency: 4 threads (target='dev')
11:57:38  
11:57:39  1 of 2 START sql view model main.stg_coffee_sales .............................. [RUN]
11:57:39  1 of 2 OK created sql view model main.stg_coffee_sales ......................... [OK in 0.04s]
11:57:39  2 of 2 START sql table model main.fct_daily_revenue ............................ [RUN]
11:57:39  2 of 2 OK created sql table model main.fct_daily_revenue ....................... [OK in 0.04s]
11:57:39  
11:57:39  Finished running 1 table model, 1 view model in 0 hours 0 minutes and 0.15 seconds (0.15s).
11:57:39  
11:57:39  Completed successfully
11:57:39  
11:57:39  Done. PASS=2 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=2
11:57:40  Running with dbt=1.13.0-b1
11:57:40  Registered adapter: duckdb=1.11.1
11:57:40  Found 2 models, 9 data tests, 1 source, 511 macros
11:57:40  
11:57:40  Concurrency: 4 threads (target='dev')
11:57:40  
11:57:41  4 of 9 START test not_null_stg_coffee_sales_amount ............................. [RUN]
11:57:41  3 of 9 START test not_null_fct_daily_revenue_total_transactions ................ [RUN]
11:57:41  2 of 9 START test not_null_fct_daily_revenue_total_daily_revenue ............... [RUN]
11:57:41  1 of 9 START test not_null_fct_daily_revenue_sale_date ......................... [RUN]
11:57:41  3 of 9 PASS not_null_fct_daily_revenue_total_transactions ...................... [PASS in 0.03s]
11:57:41  4 of 9 PASS not_null_stg_coffee_sales_amount ................................... [PASS in 0.04s]
11:57:41  2 of 9 PASS not_null_fct_daily_revenue_total_daily_revenue ..................... [PASS in 0.03s]
11:57:41  5 of 9 START test not_null_stg_coffee_sales_coffee_name ........................ [RUN]
11:57:41  1 of 9 PASS not_null_fct_daily_revenue_sale_date ............................... [PASS in 0.03s]
11:57:41  6 of 9 START test not_null_stg_coffee_sales_sale_date .......................... [RUN]
11:57:41  7 of 9 START test not_null_stg_coffee_sales_transaction_id ..................... [RUN]
11:57:41  8 of 9 START test unique_fct_daily_revenue_sale_date ........................... [RUN]
11:57:41  6 of 9 PASS not_null_stg_coffee_sales_sale_date ................................ [PASS in 0.02s]
11:57:41  9 of 9 START test unique_stg_coffee_sales_transaction_id ....................... [RUN]
11:57:41  5 of 9 PASS not_null_stg_coffee_sales_coffee_name .............................. [PASS in 0.02s]
11:57:41  8 of 9 PASS unique_fct_daily_revenue_sale_date ................................. [PASS in 0.02s]
11:57:41  7 of 9 PASS not_null_stg_coffee_sales_transaction_id ........................... [PASS in 0.02s]
11:57:41  9 of 9 PASS unique_stg_coffee_sales_transaction_id ............................. [PASS in 0.01s]
11:57:41  
11:57:41  Finished running 9 data tests in 0 hours 0 minutes and 0.14 seconds (0.14s).
11:57:41  
11:57:41  Completed successfully
11:57:41  
11:57:41  Done. PASS=9 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=9
=== Section D - Q5: Executing Airflow DAG with Mart Table Data Check ===

1️⃣ [Airflow Task 1: dbt_run_models] Running `dbt run`...

2️⃣ [Airflow Task 2: dbt_test_models] Running `dbt test`...

3️⃣ [Airflow Task 3: check_mart_has_data_for_today] Verifying mart table data...
Checking mart table 'main.fct_daily_revenue' for today's date (2026-11-20)...
  [Info] Static dataset ends on 2025-03-23 (current calendar date is 2026-11-20).
  [Info] Verifying mart data freshness for the latest reporting date (2025-03-23)...
✅ DATA QUALITY CHECK PASSED: 'fct_daily_revenue' has 1 record(s) for 2025-03-23 (6 transactions | $204.76 total daily revenue)!

🎉 Section D - Q5 Airflow DAG completed all 3 tasks (dbt run -> dbt test -> today's mart data check)!
```

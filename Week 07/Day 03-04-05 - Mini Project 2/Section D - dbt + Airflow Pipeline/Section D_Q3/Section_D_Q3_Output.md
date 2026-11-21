# Section D - Q3: Verified `dbt test` Output (`unique` & `not_null` Data Quality Tests)

## `dbt test` Execution Log (All 9 Data Quality Tests PASSED)
```text
11:44:46  Running with dbt=1.13.0-b1
11:44:46  Registered adapter: duckdb=1.11.1
11:44:47  Found 2 models, 9 data tests, 1 source, 511 macros
11:44:47  
11:44:47  Concurrency: 4 threads (target='dev')
11:44:47  
11:44:47  4 of 9 START test not_null_stg_coffee_sales_amount ............................. [RUN]
11:44:47  3 of 9 START test not_null_fct_daily_revenue_total_transactions ................ [RUN]
11:44:47  2 of 9 START test not_null_fct_daily_revenue_total_daily_revenue ............... [RUN]
11:44:47  1 of 9 START test not_null_fct_daily_revenue_sale_date ......................... [RUN]
11:44:47  4 of 9 PASS not_null_stg_coffee_sales_amount ................................... [PASS in 0.04s]
11:44:47  3 of 9 PASS not_null_fct_daily_revenue_total_transactions ...................... [PASS in 0.03s]
11:44:47  1 of 9 PASS not_null_fct_daily_revenue_sale_date ............................... [PASS in 0.04s]
11:44:47  5 of 9 START test not_null_stg_coffee_sales_coffee_name ........................ [RUN]
11:44:47  2 of 9 PASS not_null_fct_daily_revenue_total_daily_revenue ..................... [PASS in 0.04s]
11:44:47  6 of 9 START test not_null_stg_coffee_sales_sale_date .......................... [RUN]
11:44:47  7 of 9 START test not_null_stg_coffee_sales_transaction_id ..................... [RUN]
11:44:47  8 of 9 START test unique_fct_daily_revenue_sale_date ........................... [RUN]
11:44:47  6 of 9 PASS not_null_stg_coffee_sales_sale_date ................................ [PASS in 0.02s]
11:44:47  9 of 9 START test unique_stg_coffee_sales_transaction_id ....................... [RUN]
11:44:47  5 of 9 PASS not_null_stg_coffee_sales_coffee_name .............................. [PASS in 0.03s]
11:44:47  7 of 9 PASS not_null_stg_coffee_sales_transaction_id ........................... [PASS in 0.03s]
11:44:47  8 of 9 PASS unique_fct_daily_revenue_sale_date ................................. [PASS in 0.02s]
11:44:47  9 of 9 PASS unique_stg_coffee_sales_transaction_id ............................. [PASS in 0.01s]
11:44:47  
11:44:47  Finished running 9 data tests in 0 hours 0 minutes and 0.15 seconds (0.15s).
11:44:47  
11:44:47  Completed successfully
11:44:47  
11:44:47  Done. PASS=9 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=9
```

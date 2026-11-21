# Section D - Q2: Verified `dbt run` Output (`fct_daily_revenue` Mart Model)

## 1. `dbt run --select fct_daily_revenue` Execution Log
```text
11:44:44  Running with dbt=1.13.0-b1
11:44:44  Registered adapter: duckdb=1.11.1
11:44:45  Found 2 models, 9 data tests, 1 source, 511 macros
11:44:45  
11:44:45  Concurrency: 4 threads (target='dev')
11:44:45  
11:44:45  1 of 1 START sql table model main.fct_daily_revenue ............................ [RUN]
11:44:45  1 of 1 OK created sql table model main.fct_daily_revenue ....................... [OK in 0.06s]
11:44:45  
11:44:45  Finished running 1 table model in 0 hours 0 minutes and 0.14 seconds (0.14s).
11:44:45  
11:44:45  Completed successfully
11:44:45  
11:44:45  Done. PASS=1 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=1
```

## 2. Preview of Built Mart Table (`main.fct_daily_revenue` — First 10 Days)
```text
┌────────────┬────────────────────┬─────────────────────┬───────────────────────┬───────────────┬───────────────┐
│ sale_date  │ total_transactions │ total_daily_revenue │ avg_transaction_value │ card_revenue  │ cash_revenue  │
│    date    │       int64        │    decimal(38,2)    │        double         │ decimal(38,2) │ decimal(38,2) │
├────────────┼────────────────────┼─────────────────────┼───────────────────────┼───────────────┼───────────────┤
│ 2024-03-01 │                 11 │              396.30 │                 36.03 │        396.30 │          0.00 │
│ 2024-03-02 │                  7 │              228.10 │                 32.59 │        188.10 │         40.00 │
│ 2024-03-03 │                 10 │              349.10 │                 34.91 │        309.10 │         40.00 │
│ 2024-03-04 │                  4 │              135.20 │                  33.8 │        135.20 │          0.00 │
│ 2024-03-05 │                  9 │              338.50 │                 37.61 │        338.50 │          0.00 │
│ 2024-03-06 │                  5 │              170.20 │                 34.04 │        135.20 │         35.00 │
│ 2024-03-07 │                  6 │              220.10 │                 36.68 │        140.10 │         80.00 │
│ 2024-03-08 │                  8 │              265.50 │                 33.19 │        265.50 │          0.00 │
│ 2024-03-09 │                 14 │              479.40 │                 34.24 │        439.40 │         40.00 │
│ 2024-03-10 │                  7 │              231.60 │                 33.09 │         91.60 │        140.00 │
└────────────┴────────────────────┴─────────────────────┴───────────────────────┴───────────────┴───────────────┘
  10 rows                                                                                             6 columns
```

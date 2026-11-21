# Section D - Q1: Verified `dbt run` Output (`stg_coffee_sales` Staging Model)

## 1. `dbt run --select stg_coffee_sales` Execution Log
```text
11:44:42  Running with dbt=1.13.0-b1
11:44:43  Registered adapter: duckdb=1.11.1
11:44:43  Found 2 models, 9 data tests, 1 source, 511 macros
11:44:43  
11:44:43  Concurrency: 4 threads (target='dev')
11:44:43  
11:44:43  1 of 1 START sql view model main.stg_coffee_sales .............................. [RUN]
11:44:43  1 of 1 OK created sql view model main.stg_coffee_sales ......................... [OK in 0.04s]
11:44:43  
11:44:43  Finished running 1 view model in 0 hours 0 minutes and 0.12 seconds (0.12s).
11:44:43  
11:44:43  Completed successfully
11:44:43  
11:44:43  Done. PASS=1 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=1
```

## 2. Preview of Built Staging View (`main.stg_coffee_sales` — First 10 Rows)
```text
┌────────────────┬────────────┬────────────────────────┬───┬─────────────────────┬───────────────┬─────────────────────┐
│ transaction_id │ sale_date  │     sale_timestamp     │ … │       card_id       │    amount     │     coffee_name     │
│     int64      │    date    │       timestamp        │ … │       varchar       │ decimal(10,2) │       varchar       │
├────────────────┼────────────┼────────────────────────┼───┼─────────────────────┼───────────────┼─────────────────────┤
│              1 │ 2024-03-01 │ 2024-03-01 10:15:50.52 │ … │ ANON-0000-0000-0001 │         38.70 │ Latte               │
│              2 │ 2024-03-01 │ 2024-03-01 12:19:22.5… │ … │ ANON-0000-0000-0002 │         38.70 │ Hot Chocolate       │
│              3 │ 2024-03-01 │ 2024-03-01 12:20:18.0… │ … │ ANON-0000-0000-0002 │         38.70 │ Hot Chocolate       │
│              4 │ 2024-03-01 │ 2024-03-01 13:46:33.0… │ … │ ANON-0000-0000-0003 │         28.90 │ Americano           │
│              5 │ 2024-03-01 │ 2024-03-01 13:48:14.6… │ … │ ANON-0000-0000-0004 │         38.70 │ Latte               │
│              6 │ 2024-03-01 │ 2024-03-01 15:39:47.7… │ … │ ANON-0000-0000-0005 │         33.80 │ Americano with Milk │
│              7 │ 2024-03-01 │ 2024-03-01 16:19:02.7… │ … │ ANON-0000-0000-0006 │         38.70 │ Hot Chocolate       │
│              8 │ 2024-03-01 │ 2024-03-01 18:39:03.58 │ … │ ANON-0000-0000-0007 │         33.80 │ Americano with Milk │
│              9 │ 2024-03-01 │ 2024-03-01 19:22:01.7… │ … │ ANON-0000-0000-0008 │         38.70 │ Cocoa               │
│             10 │ 2024-03-01 │ 2024-03-01 19:23:15.8… │ … │ ANON-0000-0000-0008 │         33.80 │ Americano with Milk │
└────────────────┴────────────┴────────────────────────┴───┴─────────────────────┴───────────────┴─────────────────────┘
  10 rows                                                                                          7 columns (6 shown)
```

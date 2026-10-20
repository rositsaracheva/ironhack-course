# Week 3 — Day 1: ETL, ELT, and Pipeline Architecture

## Practice Workbook: BritMart Pipeline Architecture

> ### Today's Core Concepts
>
> ---
>
> #### 1. What is a Data Pipeline?
> - **In simple words:** A data pipeline is an automated, repeatable sequence of steps that moves data from source systems (tills, online store, loyalty apps, stock warehouses) to a destination where it can be queried and trusted.
> - **Real-world analogy:** Think of fresh tap water. Water is collected from reservoirs (sources), pumped through filtration and treatment stations (ingestion and cleaning), tested for quality (validation), and finally delivered to your kitchen tap ready to drink (analytics).
>
> ---
>
> #### 2. ETL vs. ELT (When Does Transformation Happen?)
> - **ETL (Extract → Transform → Load):**
>   - **What happens:** Data is extracted from sources, cleaned/transformed in a separate processing engine *before* it is loaded into the final destination.
>   - **When to use:** When you must remove sensitive fields (passwords, credit card numbers) before loading, when the destination only accepts strict clean tables, or when the target system lacks processing power.
> - **ELT (Extract → Load → Transform):**
>   - **What happens:** Raw data is extracted and loaded directly into storage first (like a data lake or modern cloud warehouse), and then transformed inside the destination using its own compute power (e.g. SQL).
>   - **When to use:** When using modern analytical databases (Snowflake, BigQuery, Databricks) that have massive compute, or when you want to retain raw historical data so multiple teams can re-transform it later.
>
> ---
>
> #### 3. Batch vs. Streaming Processing
> - **Batch Processing:**
>   - **In simple words:** Collecting records over a period of time (e.g. hourly, daily, monthly) and processing them together as a single group.
>   - **Example:** Ingesting store till transactions once every night at 01:00 for next-day morning reporting.
> - **Streaming Processing:**
>   - **In simple words:** Processing individual records or small events continuously as they arrive, with delays measured in seconds or milliseconds.
>   - **Example:** Real-time credit card fraud detection or live website user-click tracking.
>
> ---
>
> #### 4. The Four Pipeline Layers
> 1. **Raw Layer:** Preserves the incoming source data exactly as received (original format, file names, ingestion timestamps) without alterations.
> 2. **Staging Layer:** Prepares the data technically (standardising column names into `snake_case`, converting data types like text to numeric, stripping whitespace).
> 3. **Transformation Layer:** Applies business logic, cleans invalid rows, deduplicates, joins with lookup tables, and calculates business metrics.
> 4. **Analytics Layer:** The final presentation layer with pre-aggregated, trusted tables ready for BI dashboards and analysts (e.g. `daily_sales`).
>
> ---
>
> #### 5. Pipeline Reliability & Operations
> - **Dependencies:** Directing the order of execution. A downstream task (e.g. `build_daily_sales`) must never run before its upstream dependency (`clean_orders`) completes successfully.
> - **Idempotency:** A pipeline task is idempotent if running it once or running it five times produces the exact same result without duplicate rows.
> - **Retries vs. Root Cause Fixes:**
>   - **Retry:** Automatically re-attempt temporary/transient failures (e.g. a 5-second network drop).
>   - **Root Cause Fix:** Permanent failures (syntax errors, missing columns in source file) require fixing the code or data first—retrying without fixing will fail every time.
> - **Backfills:** Deliberately reprocessing missed or corrupted historical dates in chronological order, with duplicate safeguards in place.

---

## Part 1 — ETL and ELT

### Q. 1 — Perform a Small ETL Flow

A supplier sends this data:

```python
import pandas as pd

source = pd.DataFrame({
    "product_id": [101, 102, 103, 104],
    "price_gbp": ["25.50", "invalid", "12.00", "40.00"],
})
```

#### Requirements:
- `price_gbp` must be numeric.
- Invalid prices must be rejected.
- Only valid rows must be loaded into `clean_products`.

#### Python Solution:

```python
import pandas as pd

# 1. Source data received from supplier
source = pd.DataFrame({
    "product_id": [101, 102, 103, 104],
    "price_gbp": ["25.50", "invalid", "12.00", "40.00"],
})

# 2. Make a working copy so we don't change the original source
working = source.copy()

# 3. Transform: convert prices to numbers.
# "coerce" tells pandas to turn invalid text like "invalid" into NaN (missing value)
working["price_gbp"] = pd.to_numeric(
    working["price_gbp"],
    errors="coerce",
)

# 4. Filter: keep only valid rows (where price_gbp is not NaN)
clean_products = working[
    working["price_gbp"].notna()
].copy()

# 5. Separate rejected rows for audit
rejected_products = working[
    working["price_gbp"].isna()
].copy()

print("Clean rows:")
print(clean_products)

print("\nRejected rows:")
print(rejected_products)
```

#### Output:

```text
Clean rows:
   product_id  price_gbp
0         101       25.5
2         103       12.0
3         104       40.0

Rejected rows:
   product_id  price_gbp
1         102        NaN
```

> 💡 **Notes & Explanations:**
> - In an **ETL** flow, the data is cleaned and transformed **before** loading it into the clean destination table.
> - `pd.to_numeric(..., errors="coerce")` is our standard pandas tool for safely converting string columns to float numbers. Anything that cannot be converted becomes `NaN`.
> - `notna()` filters for rows that have valid numbers, while `isna()` captures the bad rows so they don't corrupt downstream tables.

---

### Q. 2 — Simulate a Small ELT Flow

Use:

```python
import pandas as pd

source = pd.DataFrame({
    "order_id": [201, 202, 203],
    "amount_gbp": ["45.50", "30.00", "bad"],
})
```

#### Requirements:
- Create `raw_orders` by copying all source rows first.
- Create `clean_orders` by converting the amount to numeric and removing invalid rows.

#### Python Solution:

```python
import pandas as pd

source = pd.DataFrame({
    "order_id": [201, 202, 203],
    "amount_gbp": ["45.50", "30.00", "bad"],
})

# Step 1: In ELT, we LOAD all source data directly into raw storage first
raw_orders = source.copy()

# Step 2: Now TRANSFORM the data directly from the raw table
clean_orders = raw_orders.copy()

# Convert amount_gbp to numeric, turning bad values into NaN
clean_orders["amount_gbp"] = pd.to_numeric(
    clean_orders["amount_gbp"],
    errors="coerce",
)

# Keep only rows that have valid amounts
clean_orders = clean_orders[
    clean_orders["amount_gbp"].notna()
].copy()

print("Raw:")
print(raw_orders)

print("\nClean:")
print(clean_orders)
```

#### Output:

```text
Raw:
   order_id amount_gbp
0       201      45.50
1       202      30.00
2       203        bad

Clean:
   order_id  amount_gbp
0       201        45.5
1       202        30.0
```

> 💡 **Notes & Explanations:**
> - The key difference between ETL and ELT is **where and when the transformation happens**.
> - Here, we saved all incoming records (including the `"bad"` row) into `raw_orders` first. Only afterwards did we clean it to create `clean_orders`.
> - This is ELT: **Extract** from source → **Load** into raw storage → **Transform** inside the destination.

---

### Q. 3 — Choose ETL or ELT

Choose the better starting pattern:

| Requirement | ETL or ELT? | Reason |
| :--- | :--- | :--- |
| **Invalid data must be removed before it reaches the target** | **ETL** | Transformation and filtering must happen before the destination receives any data. |
| **Raw source data should be kept first for later reprocessing** | **ELT** | Source data is loaded into storage first, so we can re-transform or audit it later without contacting the source again. |
| **Target system has strong SQL transformation capability** | **ELT** | The target database (e.g. Snowflake, BigQuery) has powerful compute engines designed to run large transformations quickly. |
| **Sensitive fields must be removed before loading** | **ETL** | For security and privacy (GDPR), sensitive columns must be masked or deleted before entering the target warehouse. |

---

### Q. 4 — MCQ: ETL

Which sequence represents ETL?

- **A.** Extract → Load → Transform
- **B.** Transform → Extract → Load
- **C.** Extract → Transform → Load
- **D.** Load → Extract → Transform

#### Solution:
**Correct answer: C**

---

## Part 2 — Batch, Streaming, and Raw Data

### Q. 5 — Process Three Independent Batches

Use:

```python
batches = {
    "batch_1": [10, 20, 30],
    "batch_2": [40, 50],
    "batch_3": [60, 70, 80],
}
```

#### Requirements:
For each batch, print:
- batch name
- row count
- batch total

#### Python Solution:

```python
batches = {
    "batch_1": [10, 20, 30],
    "batch_2": [40, 50],
    "batch_3": [60, 70, 80],
}

# Loop through the dictionary using .items() to get both key and list of values
for batch_name, values in batches.items():
    print(
        batch_name,
        "rows =",
        len(values),
        "total =",
        sum(values),
    )
```

#### Output:

```text
batch_1 rows = 3 total = 60
batch_2 rows = 2 total = 90
batch_3 rows = 3 total = 210
```

> 💡 **Notes & Explanations:**
> - Each batch represents an independent chunk of work.
> - `len(values)` gives the number of records (rows) in the batch.
> - `sum(values)` calculates the total numerical value in that batch.

---

### Q. 6 — Batch or Streaming?

Choose the better processing style for each scenario:

1. **Supplier sends one file every night.** -> **Batch**
   - *Why:* Files arrive periodically once per day as a completed set of records.
2. **Payment events arrive continuously and need a result within seconds.** -> **Streaming**
   - *Why:* The business needs immediate low-latency detection (e.g. fraud checking).
3. **Finance produces one monthly report.** -> **Batch**
   - *Why:* The report is only needed on a schedule once per month.
4. **Website click events arrive throughout the day.** -> **Streaming**
   - *Why:* Clicks happen continuously as users navigate the website.


---

### Q. 7 — Preserve Raw Input Before Cleaning

Use:

```python
import pandas as pd

source = pd.DataFrame({
    "order_id": [301, 302, 303],
    "city": [" London ", None, "Leeds"],
    "amount_gbp": [45.50, 20.00, -5.00],
})
```

#### Requirements:
- Create `raw_orders` and `clean_orders`.
- Rules for `clean_orders`:
  1. city must not be missing.
  2. amount must be positive (`> 0`).
  3. trim spaces from city names.
- Confirm that `raw_orders` still has all original rows.

#### Python Solution:

```python
import pandas as pd

source = pd.DataFrame({
    "order_id": [301, 302, 303],
    "city": [" London ", None, "Leeds"],
    "amount_gbp": [45.50, 20.00, -5.00],
})

# 1. Preserve the full raw copy unchanged
raw_orders = source.copy()

# 2. Filter for valid rows: city is not null and amount is positive (> 0)
clean_orders = source[
    source["city"].notna()
    & (source["amount_gbp"] > 0)
].copy()

# 3. Clean string values: remove leading and trailing whitespace
clean_orders["city"] = clean_orders["city"].str.strip()

print("Raw rows:", len(raw_orders))
print("Clean rows:", len(clean_orders))

print("\nRaw orders:")
print(raw_orders)

print("\nClean orders:")
print(clean_orders)
```

#### Output:

```text
Raw rows: 3
Clean rows: 1

Raw orders:
   order_id      city  amount_gbp
0       301   London        45.50
1       302      None       20.00
2       303     Leeds       -5.00

Clean orders:
   order_id    city  amount_gbp
0       301  London        45.5
```

> 💡 **Notes & Explanations:**
> - Preserving `raw_orders` is a core data engineering best practice. If business rules change in the future, we still have the original 3 rows.
> - In `clean_orders`, order `302` was rejected because the city was missing (`None`), and order `303` was rejected because the amount was negative (`-5.00`).
> - Order `301` was kept, and `" London "` was trimmed cleanly to `"London"`.

---

### Q. 8 — MCQ: Streaming

Which requirement is the strongest reason to use streaming?

- **A.** Fraud events must be checked within seconds.
- **B.** One CSV file arrives every Sunday.
- **C.** A report is needed once per quarter.
- **D.** A yearly archive is created.

#### Solution:
**Correct answer: A**

> 💡 **Notes & Explanations:**
> - Streaming is only worth the extra operational complexity when **freshness (seconds/milliseconds)** is critical to the business.
> - Periodic reports (weekly, quarterly, yearly) should always use batch processing.

---

## Part 3 — Staging, Transformation, and Analytics Layers

### Q. 9 — Place Work in the Correct Layer

Classify each activity as mainly **staging**, **transformation**, or **analytics**:

- **A. Rename source columns to standard names.** -> **Staging**
- **B. Join orders to customers.** -> **Transformation**
- **C. Calculate daily revenue by city.** -> **Analytics**
- **D. Convert an amount column from text to numeric.** -> **Staging** *(or transformation depending on design)*
- **E. Create a report-ready monthly sales table.** -> **Analytics**



> 💡 **Notes & Explanations:**
> - **Staging Layer:** Technical preparation (standardise column names, cast types, strip whitespace).
> - **Transformation Layer:** Business logic (join tables, deduplicate, filter by business status).
> - **Analytics Layer:** Aggregated metrics built specifically for reporting and dashboards.

---

### Q. 10 — Build a Staging Output

Use:

```python
import pandas as pd

source = pd.DataFrame({
    "OrderID": [401, 402, 403],
    "CustomerID": [1, 2, 1],
    "Amount": ["45.50", "30.00", "20.00"],
})
```

#### Requirements:
- Create a staging DataFrame with standard column names:
  - `order_id`
  - `customer_id`
  - `amount_gbp`
- Convert `amount_gbp` to numeric.

#### Python Solution:

```python
import pandas as pd

source = pd.DataFrame({
    "OrderID": [401, 402, 403],
    "CustomerID": [1, 2, 1],
    "Amount": ["45.50", "30.00", "20.00"],
})

# 1. Rename columns to standard lowercase snake_case
staging = source.rename(columns={
    "OrderID": "order_id",
    "CustomerID": "customer_id",
    "Amount": "amount_gbp",
}).copy()

# 2. Convert amount_gbp from text string to float numbers
staging["amount_gbp"] = pd.to_numeric(
    staging["amount_gbp"],
    errors="raise", # will throw an error if an unexpected bad value is encountered
)

print(staging)
```

#### Output:

```text
   order_id  customer_id  amount_gbp
0       401            1        45.5
1       402            2        30.0
2       403            1        20.0
```

> 💡 **Notes & Explanations:**
> - Staging ensures that differences in external source file naming (like `OrderID` vs `order_id`) are unified early so the rest of the pipeline always sees standard column names.

---

### Q. 11 — Build an Analytics Output

Use this complete dataset:

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [501, 502, 503, 504],
    "city": ["London", "Leeds", "London", "Manchester"],
    "amount_gbp": [45.50, 30.00, 62.25, 50.00],
    "status": ["complete", "complete", "complete", "cancelled"],
})
```

#### Requirements:
- Create a report containing:
  - `city`
  - `completed_revenue_gbp`
- Expected London total: `107.75`

#### Python Solution:

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [501, 502, 503, 504],
    "city": ["London", "Leeds", "London", "Manchester"],
    "amount_gbp": [45.50, 30.00, 62.25, 50.00],
    "status": ["complete", "complete", "complete", "cancelled"],
})

# 1. Filter only completed orders (exclude cancelled ones)
completed = orders[
    orders["status"] == "complete"
].copy()

# 2. Group by city and sum up the revenue
report = (
    completed
    .groupby("city", as_index=False)
    .agg(
        completed_revenue_gbp=(
            "amount_gbp",
            "sum",
        )
    )
)

print(report)
```

#### Output:

```text
     city  completed_revenue_gbp
0   Leeds                  30.00
1  London                 107.75
```

> 💡 **Notes & Explanations:**
> - In London, orders `501` (45.50) and `503` (62.25) were completed: `45.50 + 62.25 = 107.75`.
> - Order `504` in Manchester was cancelled, so it was filtered out of the revenue report.
> - `as_index=False` keeps `city` as a regular column instead of an index.

---

### Q. 12 — MCQ: Staging

Which task is most suitable for a staging layer?

- **A.** Build the final executive KPI table.
- **B.** Create a dashboard colour theme.
- **C.** Train a machine-learning model.
- **D.** Rename and standardise source columns before deeper transformation.

#### Solution:
**Correct answer: D**

> 💡 **Notes & Explanations:**
> - Staging handles structural preparation (cleaning column names, converting types) before any complex business calculations happen.

---

## Part 4 — Dependencies, Retries, and Backfills

### Q. 13 — Put the Jobs in Order

BritMart has these jobs:
- `load_source`
- `clean_orders`
- `build_daily_sales`
- `publish_report`

#### Solution:

```text
load_source
    ↓
clean_orders
    ↓
build_daily_sales
    ↓
publish_report
```

> 💡 **Notes & Explanations:**
> - **Dependency Rule:** A job cannot run until its required inputs exist and have been validated.
> - You must first load the data (`load_source`), then clean it (`clean_orders`), then aggregate it (`build_daily_sales`), and only then make it visible to the business (`publish_report`).

---

### Q. 14 — Retry or Fix First?

Choose whether an automatic retry is useful:

| Failure | Retry useful? | Reason |
| :--- | :--- | :--- |
| **Temporary network timeout** | **Yes** | The glitch is temporary and the network connection may recover a few seconds later. |
| **Python syntax error** | **No** | Code has a syntax error; retrying 100 times will still fail until the developer fixes the typo in code. |
| **Database unavailable for 30 seconds** | **Yes** | The database might be restarting or momentarily busy; it will accept queries once it is back up. |
| **Required column removed from source file** | **No** | The schema has changed; retrying will not bring the column back. The pipeline or supplier must be fixed first. |



---

### Q. 15 — Plan a Backfill

The daily pipeline did not run on:
- `2026-08-05`
- `2026-08-06`
- `2026-08-07`

Create a backfill plan including:
- processing order
- duplicate check
- validation after each date

#### Solution:

A safe step-by-step backfill plan:

1. **Verify inputs:** Check that raw source data/files exist for all three missed dates (`2026-08-05`, `2026-08-06`, `2026-08-07`).
2. **Check for partial outputs:** Verify if any failed or partial runs already wrote records for those dates to prevent duplicates.
3. **Process sequentially in chronological order:**
   - Run the pipeline for `2026-08-05`.
   - Validate row count and total revenue for `2026-08-05`.
   - Run the pipeline for `2026-08-06`.
   - Validate row count and total revenue for `2026-08-06`.
   - Run the pipeline for `2026-08-07`.
   - Validate row count and total revenue for `2026-08-07`.
4. **Ensure idempotency:** Confirm that the pipeline uses partition overwrite or delete-then-insert for the target date so rerunning never creates duplicates.

> 💡 **Notes & Explanations:**
> - A backfill should be run in chronological order (oldest to newest) to preserve proper business sequences.
> - Validating row counts and totals after each date ensures an error is caught immediately rather than snowballing into subsequent dates.

---

### Q. 16 — MCQ: Dependency

Why is a dependency needed between `clean_orders` and `build_daily_sales`?

- **A.** To make both jobs use the same file name.
- **B.** To ensure the sales summary waits for clean data.
- **C.** To guarantee that failures can never happen.
- **D.** To remove the need for validation.

#### Solution:
**Correct answer: B**

> 💡 **Notes & Explanations:**
> - `build_daily_sales` needs trusted, clean order data to calculate accurate sales numbers. The dependency ensures it does not start until `clean_orders` completes successfully.

---

## Optional Practice

### Q. 17 — Build a Complete Independent ETL Script

Use:

```python
import pandas as pd

source = pd.DataFrame({
    "order_id": [601, 602, 603, 604],
    "city": ["London", None, "Leeds", "Manchester"],
    "amount_gbp": ["45.50", "30.00", "bad", "50.00"],
    "status": ["complete", "complete", "complete", "cancelled"],
})
```

#### Requirements:
- Create `raw_orders`, `clean_orders`, and `daily_sales`.
- Rules:
  1. Keep the raw copy unchanged.
  2. Reject missing city.
  3. Reject non-numeric amount.
  4. Use only completed orders in `daily_sales`.
  5. Aggregate revenue by city.

#### Python Solution:

```python
import pandas as pd

source = pd.DataFrame({
    "order_id": [601, 602, 603, 604],
    "city": ["London", None, "Leeds", "Manchester"],
    "amount_gbp": ["45.50", "30.00", "bad", "50.00"],
    "status": ["complete", "complete", "complete", "cancelled"],
})

# 1. Raw Layer: Keep an exact copy of the source untouched
raw_orders = source.copy()

# 2. Staging / Working copy: Convert amount_gbp to numeric
working = raw_orders.copy()
working["amount_gbp"] = pd.to_numeric(
    working["amount_gbp"],
    errors="coerce",
)

# 3. Clean Layer: Reject rows with missing city OR invalid amount
clean_orders = working[
    working["city"].notna()
    & working["amount_gbp"].notna()
].copy()

# 4. Analytics Layer: Filter for completed orders and aggregate by city
completed = clean_orders[
    clean_orders["status"] == "complete"
].copy()

daily_sales = (
    completed
    .groupby("city", as_index=False)
    .agg(
        revenue_gbp=("amount_gbp", "sum")
    )
)

print("Raw:")
print(raw_orders)

print("\nClean:")
print(clean_orders)

print("\nDaily sales:")
print(daily_sales)
```

#### Output:

```text
Raw:
   order_id        city amount_gbp     status
0       601      London      45.50   complete
1       602        None      30.00   complete
2       603       Leeds        bad   complete
3       604  Manchester      50.00  cancelled

Clean:
   order_id        city  amount_gbp     status
0       601      London        45.5   complete
3       604  Manchester        50.0  cancelled

Daily sales:
     city  revenue_gbp
0  London         45.5
```

> 💡 **Notes & Explanations:**
> - `raw_orders`: Preserves all 4 original rows.
> - `clean_orders`: Row 602 is dropped because `city` is `None`. Row 603 is dropped because `"bad"` becomes `NaN`.
> - `daily_sales`: Row 604 is dropped because its status is `"cancelled"`. Only London (order 601, amount 45.50) is included in the final sales summary.

---

### Q. 18 — Find the Pipeline Design Problem

A team runs:

```text
publish_report
build_daily_sales
clean_orders
load_source
```

in that order.

Explain the problem and provide the correct order.

#### Solution:
- **The Problem:** The sequence is executed completely in reverse!
  - You cannot publish a report before the daily sales table exists.
  - You cannot build daily sales before orders are cleaned.
  - You cannot clean orders before loading data from the source.
- **Correct Order:**

```text
load_source
    ↓
clean_orders
    ↓
build_daily_sales
    ↓
publish_report
```

---

### Q. 19 — Check Whether a Backfill Is Safe

A backfill script always uses `append` when writing results.
If `2026-08-05` is accidentally processed twice, the same rows may appear twice.

Explain why this is risky and what the team should check before rerunning.

#### Solution:
- **Why it is risky:** Blind `append` simply inserts all rows without checking if they already exist. Rerunning a date creates duplicate transactions, which doubles sales numbers and invalidates business reports.
- **What the team should check before rerunning:**
  1. **Existing data:** Check if records for that date already exist in the target table.
  2. **Idempotent write strategy:** Use partition overwrite (`mode="overwrite"`) or delete existing records for that date before inserting.
  3. **Unique keys:** Enforce primary or unique keys on `order_id` to block duplicate inserts.
  4. **Post-run reconciliation:** Compare row count and total revenue before and after running to ensure numbers are accurate.

---

### Q. 20 — Design a Four-Layer Batch Pipeline

Design an independent pipeline containing:
- `raw`
- `staging`
- `transformation`
- `analytics`

Use a daily order file as the source. For each layer, write: input, main work, output, one validation.

#### Solution:

| Layer | Input | Main Work | Output | One Validation |
| :--- | :--- | :--- | :--- | :--- |
| **Raw** | Daily order file (CSV/JSON) | Store file exactly as received with ingestion timestamp | `raw_orders` | Check file is not empty and verify input row count |
| **Staging** | `raw_orders` | Standardise column names (snake_case) and cast types | `staged_orders` | Check that required columns exist and data types are valid |
| **Transformation** | `staged_orders` | Deduplicate, apply business rules, filter valid orders | `trusted_orders` | Verify that `valid_count + rejected_count == input_count` |
| **Analytics** | `trusted_orders` | Aggregate metrics (revenue by store, city, or date) | `daily_sales_summary` | Reconcile aggregated revenue against the sum of trusted orders |

> 💡 **Notes & Explanations:**
> - Organizing pipelines into these 4 distinct layers ensures high data quality, clear debugging, and easier maintenance across the engineering team.

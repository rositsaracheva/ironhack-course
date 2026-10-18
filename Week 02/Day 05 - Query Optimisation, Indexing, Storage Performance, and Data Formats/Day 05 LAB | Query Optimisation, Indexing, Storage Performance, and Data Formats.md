# Week 2 — Day 5: Query Optimisation, Indexing, Storage Performance, and Data Formats

## Practice Workbook: BritMart Performance & Storage Optimisation

> ### Today's Core Concepts:
>
> ---
>
> #### 1. The Core Golden Rule of Performance
> - **In simple words:** *"Don't read what you don't need."*
> - Before buying a bigger, more expensive computer (adding compute / RAM / CPU), first make sure your query isn't reading millions of unnecessary rows or downloading dozens of columns you never use.
> - **The Goal:** Reduce the amount of data read, moved across the network, and held in memory.
>
> ---
>
> #### 2. Full Table Scan vs. Indexing
> - **Full Table Scan (Reading the whole book):**
>   - The database reads every single row in the table from top to bottom to find matches.
>   - *When is it fine?* When the table is tiny (e.g., 10 rows), or when you truly need almost all rows (e.g., calculating total sales for the whole company).
>   - *When is it bad?* When you have 10 million orders and just want order `#5001`.
> - **Index (The book's index at the back):**
>   - A separate lookup structure (usually a B-Tree) sorted alphabetically or numerically. It tells the database: *"Order #5001 is on shelf 4, row 12."*
>   - *Trade-off:* Every time you `INSERT`, `UPDATE`, or `DELETE`, the database must also update the index. Indexes also take up extra disk space. So only create indexes on columns you search often!
>
> ---
>
> #### 3. Selecting Columns (`SELECT *` vs. Projection)
> - **`SELECT *`:** Grabs every single column, even the huge text descriptions or shipping notes you don't care about.
> - **Projection (`SELECT col1, col2`):** Asks only for the exact columns needed.
> - In modern analytical formats (like Parquet), selecting only 3 columns out of 60 means the system physically skips reading the other 57 columns from disk!
>
> ---
>
> #### 4. Partitioning & The "Small Files" Problem
> - **Partitioning (Organising into labeled folders):**
>   - Physically splitting your data into directories by a key, like date: `/orders/year=2026/month=08/day=01/`.
>   - **Partition Pruning:** When a query says `WHERE order_date = '2026-08-01'`, the engine only opens that single folder and completely ignores the other 364 days.
> - **The Small-Files Problem:**
>   - Having 100,000 tiny files (each 100 KB) is terrible for distributed systems. Every file needs to be opened, catalogued in metadata, and scheduled as a task.
>   - It is much faster to have fewer, well-sized files (e.g., 100 files of 100 MB).
>
> ---
>
> #### 5. Row-Based vs. Columnar Storage
> - **Row-Based Storage (CSV, Avro, Traditional OLTP):**
>   - Stores row 1 completely, then row 2 completely.
>   - *Best for:* Adding new orders, fetching one complete customer record by ID.
> - **Columnar Storage (Parquet, ORC, Data Warehouses):**
>   - Stores all values of Column A together, then all values of Column B together.
>   - *Best for:* Analytics! Calculating `SUM(amount)` only reads the `amount` column numbers, without touching customer names or addresses.
>   - *Bonus:* Because all values in a column have the same type, compression works amazingly well (often 75%+ smaller).
>
> ---
>
> #### 6. The 4 Main Data Formats
> 1. **CSV:** Plain text, human-readable, simple, but slow for big data, no data types stored, no compression built-in.
> 2. **Parquet:** Binary, columnar, super fast for analytical queries, stores schema & statistics, compresses very well.
> 3. **Avro:** Binary, row-oriented, includes strict JSON schema, excellent for streaming (Kafka) and record-by-record message pipelines.
> 4. **ORC:** Binary, columnar, similar to Parquet, highly optimised for Hadoop/Hive ecosystems.

---

# Part 1 — Query Performance, Full Scans, and Indexes

## Q. 1 — Create a Table for Query Testing

### Problem:
Create the table `orders_perf` inside database `britmart_performance` with columns:
- `order_id` (INT, Primary Key)
- `customer_id` (INT, Not Null)
- `order_date` (DATE, Not Null)
- `city` (VARCHAR(50), Not Null)
- `amount_gbp` (DECIMAL(10,2), Not Null)
- `status` (VARCHAR(20), Not Null)

Then insert the 10 provided sample rows.

### Solution:

```sql
-- Step 1: Create and select the database
CREATE DATABASE IF NOT EXISTS britmart_performance;
USE britmart_performance;

-- Step 2: Create the table
CREATE TABLE orders_perf (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    city VARCHAR(50) NOT NULL,
    amount_gbp DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL
);

-- Step 3: Insert the sample test records
INSERT INTO orders_perf (order_id, customer_id, order_date, city, amount_gbp, status) VALUES
(1, 101, '2026-08-01', 'London', 45.50, 'complete'),
(2, 102, '2026-08-01', 'Manchester', 18.00, 'cancelled'),
(3, 101, '2026-08-02', 'London', 62.25, 'complete'),
(4, 103, '2026-08-02', 'Leeds', 30.00, 'complete'),
(5, 104, '2026-08-03', 'Bristol', 55.50, 'complete'),
(6, 102, '2026-08-03', 'Manchester', 12.00, 'pending'),
(7, 101, '2026-08-04', 'London', 80.00, 'complete'),
(8, 105, '2026-08-04', 'Leeds', 20.00, 'complete'),
(9, 106, '2026-08-05', 'Bristol', 100.00, 'complete'),
(10, 102, '2026-08-05', 'Manchester', 40.00, 'complete');
```

> 💡 **Explanatory Notes:**
> - `INT PRIMARY KEY`: Guarantees each order has a unique ID and automatically creates a clustered index on `order_id`.
> - `DECIMAL(10,2)`: Always use `DECIMAL` for money/currency instead of `FLOAT` or `DOUBLE` to avoid rounding errors.

---

## Q. 2 — Inspect a Query Before Adding an Index

### Problem:
Run `EXPLAIN` on a query filtering by `customer_id`:
```sql
EXPLAIN
SELECT
    order_id,
    order_date,
    amount_gbp
FROM orders_perf
WHERE customer_id = 101;
```
Record what MySQL shows for `type` (access type) and `possible_keys`.

### Solution:

```sql
EXPLAIN
SELECT
    order_id,
    order_date,
    amount_gbp
FROM orders_perf
WHERE customer_id = 101;
```

### Result Observed:

| id | select_type | table | type | possible_keys | key | key_len | ref | rows | Extra |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | SIMPLE | orders_perf | **ALL** | **NULL** | **NULL** | NULL | NULL | 10 | Using where |

> 💡 **Explanatory Notes:**
> - **What does `type: ALL` mean?** It means a **Full Table Scan**. MySQL has to inspect all 10 rows in the table.
> - **What does `possible_keys: NULL` mean?** MySQL has no index available on `customer_id` to quickly jump directly to customer 101.
> - **Why?** Because `customer_id` is just a standard column right now; only `order_id` has an index (via Primary Key).

---

## Q. 3 — Add an Index and Compare

### Problem:
Create an index named `idx_orders_customer` on `customer_id`. Run the same `EXPLAIN` query again and compare the output.

### Solution:

```sql
-- Create index on customer_id
CREATE INDEX idx_orders_customer
ON orders_perf(customer_id);

-- Run EXPLAIN again
EXPLAIN
SELECT
    order_id,
    order_date,
    amount_gbp
FROM orders_perf
WHERE customer_id = 101;
```

### Comparison:

| Metric | Before Index | After Index | What this means |
| :--- | :--- | :--- | :--- |
| **`type` (Access Type)** | `ALL` | `ref` (or `ALL` if small table) | `ref` means it uses a non-unique index to look up rows directly. |
| **`possible_keys`** | `NULL` | `idx_orders_customer` | MySQL now sees our index as a valid tool to find matching rows. |
| **`key` (Key used)** | `NULL` | `idx_orders_customer` | The query optimiser chose to use our new index! |
| **`rows` scanned** | `10` | `3` | Instead of scanning 10 rows, it only looks at the 3 rows belonging to customer 101. |

> 💡 **Explanatory Notes:**
> - **Note on Small Tables:** If a table only has 10 rows, MySQL's cost-based optimiser might sometimes decide that reading the 10 rows from memory (`ALL`) is faster than reading the index first and then jumping to the table. In larger production tables (thousands or millions of rows), the index will always be chosen!

---

## Q. 4 — MCQ: Index

### Question:
When is an index most likely to help?
- **A.** A query returns almost every row and needs every column.
- **B.** A query filters a large table using a selective column.
- **C.** A query never uses the indexed column.
- **D.** A table is written once and never queried.

### Solution:
**Correct Answer: B**

> 💡 **Explanatory Notes:**
> - **Selective column** means the value you search for belongs to only a small percentage of rows (e.g. searching for a specific customer or date).
> - If a query returns 95% of the table (Option A), scanning the entire table is actually faster than using an index, because reading the index back-and-forth adds unnecessary overhead.

---

# Part 2 — Filtering Early, Selecting Columns, and Join Keys

## Q. 5 — Compare `SELECT *` with Required Columns

### Problem:
Compare Query A and Query B:
- **Query A:** `SELECT * FROM orders_perf WHERE status = 'complete';`
- **Query B:** `SELECT order_id, order_date, amount_gbp FROM orders_perf WHERE status = 'complete';`

Explain why Query B is better when those are the only columns needed.

### Solution & Explanation:

```sql
-- Query A: Returns all 6 columns
SELECT *
FROM orders_perf
WHERE status = 'complete';

-- Query B: Returns only the 3 needed columns (Better Practice)
SELECT
    order_id,
    order_date,
    amount_gbp
FROM orders_perf
WHERE status = 'complete';
```

> 💡 **Explanatory Notes (Why Query B is superior):**
> 1. **Network & Memory Savings:** Query B transfers 50% fewer columns over the network and uses less memory on the database server and client machine.
> 2. **Columnar Pruning in Analytical Storage:** In formats like Parquet, the database engine literally reads zero bytes from disk for `customer_id`, `city`, and `status` (after filtering).
> 3. **Index Covering (Covering Index):** If an index contains all requested columns, the database can answer Query B entirely from the index without even touching the main table.
> 4. **Code Safety & Maintainability:** `SELECT *` breaks downstream applications if a developer adds or reorders columns in the table later.

---

## Q. 6 — Filter Before Returning Data

### Problem:
BritMart needs only:
1. `completed` orders
2. from `2026-08-03` onwards (`>=`)
3. amount at least `£40` (`>=`)

Write one query that applies all three filters.

### Solution:

```sql
SELECT
    order_id,
    customer_id,
    order_date,
    amount_gbp
FROM orders_perf
WHERE status = 'complete'
  AND order_date >= '2026-08-03'
  AND amount_gbp >= 40.00
ORDER BY order_date, order_id;
```

> 💡 **Explanatory Notes:**
> - **Predicate Pushdown / Filtering Early:** By placing all 3 conditions in the `WHERE` clause, the database evaluates the filters at storage level before returning rows.
> - Only 2 rows meet all 3 criteria (Order #5: Bristol £55.50 on 2026-08-03, Order #7: London £80.00 on 2026-08-04, and Order #9: Bristol £100.00 on 2026-08-05, plus Order #10: Manchester £40.00 on 2026-08-05).
> - Never download all records into Python or Excel and then filter them there. Always let the database engine filter first!

---

## Q. 7 — Choose the Correct Join Key

### Problem:
Create table `customers_perf` with sample customer data. Join `orders_perf` and `customers_perf` using the correct key. Explain why joining on `city` would be unsafe.

### Solution:

```sql
-- Step 1: Create customers_perf table
CREATE TABLE customers_perf (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL
);

-- Step 2: Insert sample customers
INSERT INTO customers_perf (customer_id, customer_name, city) VALUES
(101, 'Amelia Clarke', 'London'),
(102, 'Oliver Bennett', 'Manchester'),
(103, 'Aisha Khan', 'Leeds'),
(104, 'Harry Thompson', 'Bristol'),
(105, 'Emily Wilson', 'Leeds'),
(106, 'Noah Davies', 'Bristol');

-- Step 3: Join using the correct foreign key (customer_id)
SELECT
    o.order_id,
    c.customer_name,
    o.amount_gbp,
    o.status
FROM orders_perf o
INNER JOIN customers_perf c
    ON o.customer_id = c.customer_id;
```

> 💡 **Explanatory Notes (Why joining on `city` is dangerous):**
> - `customer_id` is a **Primary Key / Foreign Key** pair: it is unique and specifically identifies *who* placed the order.
> - `city` is **NOT unique**: Notice that both Aisha Khan (103) and Emily Wilson (105) live in `Leeds`. Also, Harry Thompson (104) and Noah Davies (106) live in `Bristol`.
> - If you join on `city`, an order placed in Leeds will duplicate and match **both** Aisha and Emily! This causes a "Cartesian explosion" (accidental duplicates and inflated financial revenue totals).

---

## Q. 8 — MCQ: Required Columns

### Question:
Why should a query select only the columns it needs?
- **A.** It guarantees that every query uses an index.
- **B.** It removes the need for filters.
- **C.** It can reduce unnecessary data read or transferred.
- **D.** It makes all joins disappear.

### Solution:
**Correct Answer: C**

> 💡 **Explanatory Notes:**
> - Requesting fewer columns reduces I/O disk reads, network bandwidth, and memory consumption. It does not replace filters or eliminate joins.

---

# Part 3 — Partitioning, Small Files, Columnar Storage, and Compression

## Q. 9 — Choose a Partitioning Column

### Problem:
BritMart stores several years of order data. Most business reports filter by `order_date`.
Consider: `order_id`, `order_date`, `customer_name`, `amount_gbp`.
Which is the best starting choice for partitioning? Explain why.

### Solution:
**Best Choice: `order_date`**

> 💡 **Explanatory Notes:**
> - **Partition Pruning:** Because reports almost always filter by dates (e.g. *"Show last week's sales"* or *"Show August 2026"*), the query engine can skip reading 99% of the folders on disk.
> - **Why not `order_id`?** `order_id` is unique for every row. Partitioning by `order_id` would create 1 folder per order (millions of folders with 1 row each—a total disaster!).
> - **Why not `amount_gbp`?** Continuous numerical values have too many distinct values and are rarely the primary slicing filter for storage.
> - **Rule of thumb for partitioning:** Pick a column with **controlled cardinality** (like Year, Month, or Day) that matches your **most frequent filter condition**.

---

## Q. 10 — Design a Date-Based Layout

### Problem:
BritMart has 3 daily batches:
- `2026-08-01` -> 100,000 rows
- `2026-08-02` -> 120,000 rows
- `2026-08-03` -> 90,000 rows

Create a simple directory storage layout using the date.

### Solution:

```text
orders_storage/
├── order_date=2026-08-01/
│   └── part-0001.parquet
├── order_date=2026-08-02/
│   └── part-0001.parquet
└── order_date=2026-08-03/
    └── part-0001.parquet
```

> 💡 **Explanatory Notes:**
> - This naming convention (`column_name=value`) is standard Hive-style partitioning used by Spark, AWS Athena, Snowflake, Databricks, and Google BigQuery.
> - When you run `SELECT * FROM orders WHERE order_date = '2026-08-02'`, the engine directly reads only the `order_date=2026-08-02` folder and ignores the rest.

---

## Q. 11 — Find the Small-Files Problem

### Problem:
Compare two designs storing the exact same 10 GB of data:
- **Design A:** 100 files of about 100 MB each
- **Design B:** 100,000 files of about 0.1 MB (100 KB) each

Which design is more likely to create excessive file-management and task overhead? Explain why.

### Solution:
**Design B creates the severe small-files problem.**

> 💡 **Explanatory Notes:**
> - In distributed systems (like Hadoop HDFS, AWS S3 with Spark, or Data Lakes):
>   1. **Metadata Overhead:** The system must record file name, path, block locations, and permissions for 100,000 separate files.
>   2. **Task Scheduling Overhead:** Each file often starts an individual read task or thread. Starting and stopping 100,000 tasks takes more time than actually processing the tiny 100 KB data!
>   3. **Network & Open/Close Latency:** Opening and closing an HTTP/storage connection 100,000 times wastes huge amounts of I/O time.
> - **Design A is much better:** 100 MB is a healthy file size for modern distributed analytical engines.

---

## Q. 12 — MCQ: Compression

### Question:
What is the main storage benefit of compression?
- **A.** It reduces the amount of storage required for compressible data.
- **B.** It makes every query use a primary key.
- **C.** It removes the need for data types.
- **D.** It changes row-based data into a relational database.

### Solution:
**Correct Answer: A**

> 💡 **Explanatory Notes:**
> - Compression algorithms (like Snappy, Gzip, or ZSTD) find repeating patterns and encode them using fewer bytes, significantly reducing disk space and network transfer times.
> - *The Trade-off:* Compressing and decompressing takes a little bit of CPU work, but because reading smaller files from disk/network is so much faster, compression almost always improves overall speed.

---

# Part 4 — CSV, Parquet, Avro, and ORC

## Q. 13 — Compare the Formats

### Problem:
Complete the comparative table for CSV, Parquet, Avro, and ORC.

### Solution:

| Format | Text or Binary? | Row or Column Oriented? | Common Strength / Best Use Case |
| :--- | :--- | :--- | :--- |
| **CSV** | Text | Row-oriented | Simple, human-readable, widely supported by any tool (Excel, Python). Great for small exports. |
| **Parquet** | Binary | Columnar | Super-fast analytical reads, column pruning, statistics, high compression. Standard in Data Lakes/Lakehouses. |
| **Avro** | Binary | Row-oriented | Stores schema with data, compact serialization, ideal for streaming events (Kafka) & message queues. |
| **ORC** | Binary | Columnar | Highly optimised columnar storage, strong compression and indexing, prominent in Hadoop/Hive ecosystem. |

> 💡 **Explanatory Notes:**
> - **Row formats (CSV, Avro)** write whole records at once.
> - **Columnar formats (Parquet, ORC)** group each column together, making them the kings of analytical queries (`SUM`, `AVG`, `GROUP BY`).

---

## Q. 14 — Choose a Format for Each Requirement

### Problem:
Choose **CSV**, **Parquet**, **Avro**, or **ORC** for each:
- **A.** A simple file that a business user can open easily.
- **B.** Analytical data where queries often read only a few columns.
- **C.** Record-oriented data exchange where schema travels with the data.
- **D.** Columnar analytical storage used with systems that support ORC well.

### Solution:

| Requirement | Format | Why? |
| :--- | :--- | :--- |
| **A. Simple file business user can open easily** | **CSV** | Any non-technical user can double-click a CSV and view it in Microsoft Excel or Notepad. |
| **B. Analytical data reading only a few columns** | **Parquet** | Columnar layout skips all unneeded columns and reads only the required column blocks. |
| **C. Record-oriented data exchange with schema** | **Avro** | Encodes entire rows with a built-in JSON schema contract, perfect for real-time Kafka topics. |
| **D. Columnar analytical storage for Hive/Hadoop** | **ORC** | Optimized Row Columnar format specifically tuned for Hadoop and Apache Hive stacks. |

---

## Q. 15 — Inspect a CSV and List Its Limitations

### Problem:
Inspect the sample CSV file:
```csv
order_id,order_date,city,amount_gbp,status
1,2026-08-01,London,45.50,complete
2,2026-08-01,Manchester,18.00,cancelled
3,2026-08-02,Leeds,30.00,complete
```
Answer:
1. How is the schema represented?
2. Is the file human-readable?
3. List two limitations compared with a binary analytical format (like Parquet).

### Solution:

1. **Schema representation:** The schema is weakly represented only as column names in the first line (header row). There are **no data types** specified—every value is stored simply as plain text characters (`"45.50"` is text, not explicitly a decimal).
2. **Human-readability:** **Yes**, it is plain text; you can open and read it in any standard text editor.
3. **Two main limitations compared to Parquet:**
   - **No Column Pruning:** To read just `amount_gbp`, a program must read the entire file line-by-line and parse commas across all columns.
   - **No Embedded Types or Statistics:** Every reader has to guess or cast data types (e.g. is `order_date` a string or a date?). There are no min/max statistics to skip reading rows.
   - **Larger File Size / Poor Compression:** Because it stores numbers as strings and has no columnar compression, it takes significantly more disk space.

---

## Q. 16 — MCQ: Parquet

### Question:
Why is Parquet commonly used for analytical data?
- **A.** It stores every value as plain text for manual editing.
- **B.** It is designed only for single-row transaction updates.
- **C.** It cannot store schema information.
- **D.** Its columnar layout can help queries read only needed columns.

### Solution:
**Correct Answer: D**

> 💡 **Explanatory Notes:**
> - Analytical queries (like aggregations in dashboards) typically analyze many rows across just 2 to 5 columns. Parquet's columnar layout physically reads only those requested columns from disk.

---

# Optional Practice

## Q. 17 — Build and Compare a Composite Index

### Problem:
BritMart often runs:
```sql
SELECT order_id, order_date, amount_gbp
FROM orders_perf
WHERE customer_id = 101
  AND order_date >= '2026-08-02';
```
Create a composite index on `(customer_id, order_date)`. Compare with single-column index.

### Solution:

```sql
-- Step 1: Drop the old single index if desired, or add the new composite index
DROP INDEX idx_orders_customer ON orders_perf;

-- Step 2: Create a multi-column (composite) index
CREATE INDEX idx_orders_customer_date
ON orders_perf(customer_id, order_date);

-- Step 3: Run EXPLAIN to verify execution plan
EXPLAIN
SELECT
    order_id,
    order_date,
    amount_gbp
FROM orders_perf
WHERE customer_id = 101
  AND order_date >= '2026-08-02';
```

> 💡 **Explanatory Notes (How Composite Indexes work):**
> - **The Phone Book Analogy:** Think of a phone book sorted by `(LastName, FirstName)`. You can quickly find `"Smith, John"`.
> - Because both `customer_id` and `order_date` are in the index in that order, MySQL uses the index to filter **both** conditions at once!
> - With only a single index on `customer_id`, MySQL would find all orders for customer 101, then manually check the `order_date` row by row. With the composite index, it directly pinpoints the exact subset.

---

## Q. 18 — Find an Index That May Not Help Much

### Problem:
Consider the query:
```sql
SELECT SUM(amount_gbp)
FROM orders_perf;
```
Would an index on `customer_id` make this full-table total automatically fast? Explain why or why not.

### Solution:
**No, an index on `customer_id` will NOT help this query at all.**

> 💡 **Explanatory Notes:**
> 1. **No Filter:** The query has no `WHERE customer_id = ...` filter.
> 2. **Full Table Calculation:** The query calculates the sum of all orders across the entire company. Every single row must be read to compute the sum.
> 3. **Wrong Column:** The calculation needs `amount_gbp`, not `customer_id`.
> - **Key takeaway:** Indexes only help when you are filtering, joining, or sorting by the indexed column. Never assume adding an index magically speeds up unrelated queries!

---

## Q. 19 — Review a Poor Storage Layout

### Problem:
BritMart stores 3 years of orders as:
- One single folder
- 500,000 tiny CSV files
- No date organisation
- Reports usually filter by date and select only a few columns.

Using today's concepts, suggest 3 improvements.

### Solution:

```text
3 Recommended Improvements:

1. Organise with Date Partitioning (Partition Pruning):
   - Group the files into folders by date (e.g., /orders/year=2026/month=08/).
   - Why: Queries filtering for August 2026 won't have to scan the remaining 35 months.

2. Compact Small Files into Larger Files (Solve Small-Files Problem):
   - Consolidate the 500,000 tiny files into fewer, larger files (target 64 MB to 256 MB each).
   - Why: Reduces metadata overhead, file opening/closing latency, and task scheduling bottlenecks.

3. Convert from CSV to a Columnar Format (Parquet or ORC) with Compression:
   - Convert raw CSV into compressed Parquet (e.g. with Snappy compression).
   - Why: Enables column pruning (reading only 5 columns instead of all 60) and slashes storage size by 70-80%.
```

---

## Q. 20 — Choose the Complete Design

### Problem:
BritMart scenario:
- Daily order data
- Reports filter by date
- Reports select 5 columns from a 60-column dataset
- Data retained for several years

Choose and explain:
1. Partitioning approach
2. File format
3. Compression need
4. Query habit

### Solution:

| Design Dimension | Choice | Why this is the best decision for BritMart |
| :--- | :--- | :--- |
| **1. Partitioning Approach** | **Partition by Date (`order_date` or `year/month`)** | Since queries almost always filter on dates, partition pruning will allow engines to skip unneeded years/months completely. |
| **2. File Format** | **Apache Parquet (or ORC)** | Parquet is columnar. When queries need only 5 of the 60 columns, the engine skips 55 columns entirely, saving 90%+ of I/O. |
| **3. Compression Need** | **Yes (Snappy or ZSTD)** | Compressing column blocks drastically shrinks multi-year storage costs and speeds up reads with minimal CPU cost. |
| **4. Query Habit** | **Filter early & Select only needed columns** | Never use `SELECT *`. Always specify the 5 required columns and filter on the partitioned date column in the `WHERE` clause. |

---

## 🎯 Summary Checklist for Beginners

- [x] **Filter Early:** Always write specific `WHERE` conditions to eliminate unnecessary rows as close to the storage layer as possible.
- [x] **Project Needed Columns:** Avoid `SELECT *`. Only select the columns you actually need.
- [x] **Index Strategically:** Index columns that are frequently used in selective filters and joins; remember that indexes slow down writes and use extra storage.
- [x] **Partition by High-Usage Filter Keys:** Use date or category partitions with controlled cardinality to enable partition pruning.
- [x] **Avoid the Small Files Trap:** Strive for balanced file sizes (e.g., 64MB - 256MB) instead of thousands of tiny files.
- [x] **Pick the Right Format for the Job:** Use **CSV** for human-facing small files, **Avro** for row-based event streaming, and **Parquet/ORC** for analytical querying.

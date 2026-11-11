# Databricks Free Edition – Parquet & PySpark Lab

## Business scenario
You are a junior data engineer at a retail/e-commerce company. You have three source files:
- `customers.csv` – 120 customers
- `products.csv` – 20 products
- `orders.csv` – 1,500 order records

The data includes a few missing values to practise data-quality handling. Dates use ISO format (`YYYY-MM-DD`).

## 1. Upload the files
1. Open your Databricks Free Edition workspace.
2. Open **Catalog** and select your workspace catalog (often `workspace`).
3. Create a schema named `retail_lab` if it does not exist.
4. Create a volume named `raw_files` inside `retail_lab`.
5. Upload the three CSV files into that volume.
6. In the notebook below, replace `workspace` if your catalog has a different name.

Expected paths:
- `/Volumes/workspace/retail_lab/raw_files/customers.csv`
- `/Volumes/workspace/retail_lab/raw_files/products.csv`
- `/Volumes/workspace/retail_lab/raw_files/orders.csv`

If your workspace uses a different catalog, update the first path segment.

## 2. Create a notebook
Create a Python notebook and run the following starter code.

```python
catalog = "workspace"
schema = "retail_lab"
base = f"/Volumes/{catalog}/{schema}/raw_files"

customers = spark.read.option("header", True).option("inferSchema", True).csv(f"{base}/customers.csv")
products = spark.read.option("header", True).option("inferSchema", True).csv(f"{base}/products.csv")
orders = spark.read.option("header", True).option("inferSchema", True).csv(f"{base}/orders.csv")

display(customers.limit(5))
display(products.limit(5))
display(orders.limit(5))
```

## 3. Convert CSV to Parquet
```python
parquet_base = f"/Volumes/{catalog}/{schema}/parquet"

(customers.write.mode("overwrite").parquet(f"{parquet_base}/customers"))
(products.write.mode("overwrite").parquet(f"{parquet_base}/products"))
(orders.write.mode("overwrite").parquet(f"{parquet_base}/orders"))
```

Read one Parquet dataset back:
```python
orders_parquet = spark.read.parquet(f"{parquet_base}/orders")
orders_parquet.printSchema()
display(orders_parquet.limit(10))
```

Note: The downloadable pack contains CSV source files because Parquet is a binary columnar format and the file-generation runtime here does not have a Parquet writer installed. The notebook creates the actual Parquet datasets directly in your Databricks environment.

## 4. Register tables for SQL
```python
customers_parquet = spark.read.parquet(f"{parquet_base}/customers")
products_parquet = spark.read.parquet(f"{parquet_base}/products")
orders_parquet = spark.read.parquet(f"{parquet_base}/orders")

customers_parquet.createOrReplaceTempView("customers")
products_parquet.createOrReplaceTempView("products")
orders_parquet.createOrReplaceTempView("orders")
```
Now use a SQL cell (`%sql`) or `spark.sql(...)`.

## 5. Exercises
Try the questions first, then check `solutions.sql` and `solutions_python.py`.

### Level 1 – Basics
1. Display the first 10 orders.
2. Show the schema and row count of each dataset.
3. Find all orders with status `Delivered`.
4. Show orders placed in 2025.
5. List distinct order statuses.
6. Find orders with a missing `shipping_date`.

### Level 2 – Aggregations
7. Calculate total number of orders by status.
8. Calculate total quantity sold by product.
9. Calculate total revenue by payment method. Revenue = quantity × unit_price × (1 − discount_pct). Treat a missing discount as 0.
10. Find monthly revenue for 2025.
11. Find the top 5 customers by total order value.
12. Calculate average order value by customer segment.

### Level 3 – Joins and data quality
13. Join orders to customers and show order ID, customer name, city and region.
14. Join orders to products and calculate revenue by product category.
15. Find customers who have never placed an order.
16. Identify duplicate order IDs.
17. Replace missing discounts with 0 and verify there are no null discounts.
18. Calculate the percentage of orders in each status.

### Level 4 – Window functions and storage
19. Rank products by revenue within each category.
20. For each customer, find their most recent order using `row_number`.
21. Create a gold table containing monthly revenue by region.
22. Save the gold table as Parquet and read it back.
23. Save the cleaned orders as a Delta table and query it with SQL.
24. Compare Parquet and Delta at a high level: what extra capabilities does Delta provide?

## 6. Suggested workflow
- Complete Levels 1–2 using SQL.
- Complete Levels 3–4 using PySpark DataFrames or SQL.
- Use `display()` to inspect results.
- Use `DESCRIBE DETAIL` on a Delta table to inspect its format and location.

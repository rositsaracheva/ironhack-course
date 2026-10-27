import duckdb

# Connect to the DuckDB database inside the container
con = duckdb.connect("/opt/airflow/data/warehouse.duckdb")

# Create the raw table matching the schema in the manual
con.execute("""
CREATE TABLE IF NOT EXISTS sales_raw(
    order_id INTEGER, 
    customer VARCHAR, 
    city VARCHAR, 
    product VARCHAR, 
    quantity INTEGER, 
    price DECIMAL(10,2)
);
""")

# Refresh table with the latest CSV data
con.execute("DELETE FROM sales_raw;")
con.execute("INSERT INTO sales_raw SELECT * FROM read_csv_auto('/opt/airflow/data/sales.csv');")

count = con.execute("SELECT COUNT(*) FROM sales_raw").fetchone()[0]
print(f"Successfully loaded {count} rows into sales_raw table.")

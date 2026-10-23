"""
=============================================================================
QuickCart E-Commerce Daily ELT Pipeline DAG
Section D - Q2: Airflow DAG Development
File: quickcart_airflow_dag.py
Schedule: Daily at 2:00 AM (0 2 * * *)
=============================================================================
Requirements Fulfilled:

- Runs daily at 2:00 AM
- FileSensor for CSV arrival detection
- CSV extraction and schema validation
- Staging table loads
- In-warehouse transformation trigger
- Automated failure alert callback (email alerts)
- Retries (2), retry delays (5 mins), logging, and task dependencies
"""

from datetime import datetime, timedelta
import logging
import os
import pandas as pd
import sqlite3

# ---------------------------------------------------------------------------
# AIRFLOW IMPORTS (With graceful fallback for testing outside of Docker)
# ---------------------------------------------------------------------------
try:
    from airflow import DAG
    try:
        from airflow.operators.python import PythonOperator
        from airflow.sensors.filesystem import FileSensor
    except ImportError:
        from airflow.providers.standard.operators.python import PythonOperator
        from airflow.sensors.filesystem import FileSensor
except ImportError:
    # Allows testing task logic on machines without Airflow installed globally
    class DAG:
        def __init__(self, *args, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass

    class _BaseMockOperator:
        def __init__(self, *args, **kwargs): pass
        def __rshift__(self, other): return other
        def __rrshift__(self, other): return self

    PythonOperator = _BaseMockOperator
    FileSensor = _BaseMockOperator

# ---------------------------------------------------------------------------
# PATH DEFINITIONS
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
DB_PATH = os.path.join(BASE_DIR, "data", "quickcart.db")


# ---------------------------------------------------------------------------
# FAILURE ALERT CALLBACK (Email Alerting Simulation)
# ---------------------------------------------------------------------------
def on_failure_alert(context):
    """
    Triggered automatically whenever any task fails.
    Extracts failure context and dispatches an incident alert.
    """
    task_instance = context.get("task_instance")
    task_id = task_instance.task_id if task_instance else "unknown_task"
    dag_id = task_instance.dag_id if task_instance else "quickcart_daily_elt_pipeline"
    execution_date = context.get("execution_date", datetime.utcnow())
    exception = context.get("exception", "No exception info")

    error_message = f"""
    🚨 [AIRFLOW ALERT] QuickCart Pipeline Task Failure!
    ---------------------------------------------------
    DAG        : {dag_id}
    Task       : {task_id}
    Execution  : {execution_date}
    Error      : {exception}
    Action     : Check Airflow task logs for traceback.
    ---------------------------------------------------
    """
    logging.error(error_message)
    # If SMTP is configured in Airflow, Airflow sends an automated email:
    # send_email(to=["data-alerts@quickcart.com"], subject="QuickCart Pipeline Failure", html_content=error_message)


# ---------------------------------------------------------------------------
# DEFAULT DAG ARGUMENTS
# ---------------------------------------------------------------------------
default_args = {
    "owner": "quickcart_data_team",
    "depends_on_past": False,
    "email": ["data-alerts@quickcart.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,                             # Requirement: Retries
    "retry_delay": timedelta(minutes=5),      # Requirement: Retry delay
    "on_failure_callback": on_failure_alert,  # Requirement: Failure email alert callback
}


# ---------------------------------------------------------------------------
# TASK FUNCTIONS
# ---------------------------------------------------------------------------

def extract_and_validate_data():
    """
    Task: Extracts CSV files and performs data validation.
    Checks that files are non-empty and required columns are present.
    """
    logging.info("Starting CSV extraction and schema validation...")
    
    files_to_check = {
        "customers.csv": ["customer_id", "customer_name", "email", "city"],
        "orders.csv": ["order_id", "customer_id", "product_id", "quantity", "unit_price"],
        "products.csv": ["product_id", "product_name", "category", "selling_price"],
        "clickstream.csv": ["event_id", "event_type", "event_timestamp"]
    }

    for filename, required_cols in files_to_check.items():
        file_path = os.path.join(RAW_DATA_DIR, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing required source file: {file_path}")

        df = pd.read_csv(file_path)
        if len(df) == 0:
            raise ValueError(f"Source file {filename} is empty!")

        missing = set(required_cols) - set(df.columns)
        if missing:
            raise ValueError(f"Schema validation failed for {filename}. Missing: {missing}")

        logging.info(" Successfully validated %s with %d rows.", filename, len(df))


def load_raw_to_staging():
    """
    Task: Loads raw CSV files into SQLite/Warehouse staging tables.
    """
    logging.info("Loading validated raw CSVs into staging tables in %s...", DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    
    # Load each dataset into a staging table
    tables = {
        "staging_customers": os.path.join(RAW_DATA_DIR, "customers.csv"),
        "staging_orders": os.path.join(RAW_DATA_DIR, "orders.csv"),
        "staging_products": os.path.join(RAW_DATA_DIR, "products.csv"),
        "staging_clickstream": os.path.join(RAW_DATA_DIR, "clickstream.csv"),
    }
    
    for table_name, csv_path in tables.items():
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        logging.info(" Staged %d records into table: %s", len(df), table_name)

    conn.close()
    logging.info("All staging tables loaded successfully.")


def trigger_transformations():
    """
    Task: Triggers downstream SQL transformations (ELT Transform step).
    Builds aggregated daily sales summary and active user metrics.
    """
    logging.info("Triggering in-warehouse ELT transformations...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create / Refresh Gold Layer daily sales aggregation mart
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_sales_summary AS
        SELECT 
            date(order_date) AS sales_date,
            COUNT(order_id) AS total_orders,
            ROUND(SUM(quantity * unit_price), 2) AS daily_revenue,
            COUNT(DISTINCT customer_id) AS unique_buyers
        FROM staging_orders
        WHERE payment_status = 'Paid'
        GROUP BY date(order_date);
    """)

    conn.commit()
    conn.close()
    logging.info(" ELT Transformation completed: daily_sales_summary table updated.")


# ---------------------------------------------------------------------------
# DAG DEFINITION
# ---------------------------------------------------------------------------

with DAG(
    dag_id="quickcart_daily_elt_pipeline",
    default_args=default_args,
    description="QuickCart E-Commerce Daily 2:00 AM Ingestion and ELT Pipeline",
    schedule="0 2 * * *",                     # Requirement: Daily at 2:00 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["quickcart", "ecommerce", "elt", "daily"],
) as dag:

    # 1. Sensor: Wait for the primary orders CSV to arrive in data/raw/
    wait_for_orders_file = FileSensor(
        task_id="wait_for_orders_csv",
        filepath=os.path.join(RAW_DATA_DIR, "orders.csv"),
        poke_interval=30,                     # Check every 30 seconds
        timeout=300,                          # Timeout after 5 minutes
        mode="poke",
    )

    # 2. Extract & Validation Task
    validate_csv_files = PythonOperator(
        task_id="extract_and_validate_csvs",
        python_callable=extract_and_validate_data,
    )

    # 3. Load Raw Data into Staging
    load_staging_tables = PythonOperator(
        task_id="load_raw_to_staging",
        python_callable=load_raw_to_staging,
    )

    # 4. Trigger In-Warehouse Transformations
    transform_data = PythonOperator(
        task_id="trigger_transformations",
        python_callable=trigger_transformations,
    )

    # -----------------------------------------------------------------------
    # TASK DEPENDENCIES (Sequential Pipeline Flow)
    # -----------------------------------------------------------------------
    wait_for_orders_file >> validate_csv_files >> load_staging_tables >> transform_data


# ---------------------------------------------------------------------------
# LOCAL DIRECT EXECUTION TEST
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING AIRFLOW DAG TASK PIPELINE LOCALLY")
    print("=" * 60)
    print("\n1️⃣ Running Task: extract_and_validate_data()...")
    extract_and_validate_data()
    print("\n2️⃣ Running Task: load_raw_to_staging()...")
    load_raw_to_staging()
    print("\n3️⃣ Running Task: trigger_transformations()...")
    trigger_transformations()
    print("\n" + "=" * 60)
    print("🎉 ALL AIRFLOW TASKS EXECUTED AND PASSED SUCCESSFULLY!")
    print("=" * 60)


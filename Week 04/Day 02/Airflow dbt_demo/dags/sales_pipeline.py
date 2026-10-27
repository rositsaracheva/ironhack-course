from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

DBT_PROJECT_DIR = "/opt/airflow/dbt_project"
DBT_PROFILES_DIR = "/opt/airflow/dbt_project/profiles"

with DAG(
    dag_id="sales_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,  # Manual trigger for lab execution
    catchup=False,
    tags=["dbt", "duckdb", "sales"],
) as dag:

    # 1. Start milestone
    start = EmptyOperator(task_id="start")

    # 2. Ingest raw CSV data into DuckDB table sales_raw
    load_csv = BashOperator(
        task_id="load_csv",
        bash_command="python /opt/airflow/data/load_csv.py",
    )

    # 3. Transform data using dbt (stg_sales and customer_sales)
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR}",
    )

    # 4. Run automated data quality tests
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"dbt test --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR}",
    )

    # 5. End milestone
    end = EmptyOperator(task_id="end")

    # Pipeline dependency order:
    start >> load_csv >> dbt_run >> dbt_test >> end

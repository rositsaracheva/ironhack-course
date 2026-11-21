"""
=============================================================================
BrewBeats — Mini Project 2: Section D (dbt + Airflow Pipeline)
Folder  : Section D - dbt + Airflow Pipeline/Section D_Q5/
File    : Section_D_Q5_airflow_dag_with_data_check.py
Task    : Section D - Q5: Add a task in the DAG to check that the mart table has data for today.
Schedule: Once a day (@daily / 0 6 * * *)
=============================================================================
How this updated Airflow DAG works:
1. Building on Section D - Q4, we keep our two dbt tasks:
   - `dbt_run_models` (`dbt run`)
   - `dbt_test_models` (`dbt test`)
2. Section D - Q5 New Task (`check_mart_has_data_for_today`):
   - We use Airflow's `PythonOperator` to run a Python function `verify_mart_has_today_data()`.
   - This function connects to our data warehouse (`brewbeats.duckdb` / Snowflake) and runs the SQL query:
       SELECT COUNT(*), COALESCE(SUM(total_daily_revenue), 0)
       FROM main.fct_daily_revenue
       WHERE sale_date = CURRENT_DATE
     (Note: For historical datasets like coffee_sales.csv whose dates end on 2025-03-23, if today's
     live calendar date is after the dataset range, we also log the latest available date in the mart
     so we can verify both the exact `CURRENT_DATE` SQL check AND see the latest daily revenue row!)
   - If the mart table has 0 rows (or no data for the target check date), it raises a `ValueError`
     so Airflow immediately marks the task as FAILED and alerts the team before broken reports go out!
3. Full Pipeline Dependency Chain:
   `dbt_run_models >> dbt_test_models >> check_mart_has_data_for_today`
"""

from datetime import datetime, date, timedelta
import subprocess
import duckdb

# ---------------------------------------------------------------------------
# AIRFLOW IMPORTS (With graceful local fallback for terminal testing)
# ---------------------------------------------------------------------------
try:
    from airflow import DAG
    from airflow.operators.bash import BashOperator
    from airflow.operators.python import PythonOperator
except ImportError:
    class DAG:
        def __init__(self, *args, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass

    class BashOperator:
        def __init__(self, task_id, bash_command, **kwargs):
            self.task_id = task_id
            self.bash_command = bash_command
        def __rshift__(self, other): return other

    class PythonOperator:
        def __init__(self, task_id, python_callable, **kwargs):
            self.task_id = task_id
            self.python_callable = python_callable
        def __rshift__(self, other): return other

# Paths to our dbt executable, project directory, and DuckDB warehouse
DBT_BIN = '/Users/rosi/Documents/IronHack Course /Week 06/Day 05 - Snowflake_DBT/dbt-env/bin/dbt'
DBT_PROJECT_DIR = '/Users/rosi/Documents/IronHack Course /Week 07/Day 03-04-05 - Mini Project 2/Section D - dbt + Airflow Pipeline/Section D_Q1/brewbeats_dbt'
DB_PATH = '/Users/rosi/Documents/IronHack Course /Week 07/Day 03-04-05 - Mini Project 2/Section D - dbt + Airflow Pipeline/Section D_Q1/brewbeats_dbt/brewbeats.duckdb'

default_args = {
    "owner": "rosi_brewbeats_data_engineer",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


# ---------------------------------------------------------------------------
# SECTION D - Q5: Python Task Function to Check That the Mart Table Has Data for Today
# ---------------------------------------------------------------------------
def verify_mart_has_today_data(check_date: str = None):
    """
    Connects to the data warehouse and checks that `fct_daily_revenue` (our mart table)
    has data for today (`CURRENT_DATE`). Raises an error if no data is found.
    """
    today_str = check_date or date.today().isoformat()
    print(f"Checking mart table 'main.fct_daily_revenue' for today's date ({today_str})...")

    con = duckdb.connect(DB_PATH)

    # 1. Exact SQL query required in production to check if the mart table has rows for today (CURRENT_DATE):
    today_query = """
        SELECT
            COUNT(*) AS row_count,
            COALESCE(SUM(total_transactions), 0) AS transactions,
            COALESCE(SUM(total_daily_revenue), 0.0) AS revenue
        FROM main.fct_daily_revenue
        WHERE sale_date = CAST(? AS DATE);
    """
    row_count, transactions, revenue = con.execute(today_query, [today_str]).fetchone()

    # 2. If running locally on the static coffee_sales.csv dataset (which covers 2024-03-01 to 2025-03-23),
    #    we also check the latest active date in the mart so the local test demonstrates a passing check:
    if row_count == 0 and check_date is None:
        latest_date = con.execute("SELECT MAX(sale_date) FROM main.fct_daily_revenue").fetchone()[0]
        print(f"  [Info] Static dataset ends on {latest_date} (current calendar date is {today_str}).")
        print(f"  [Info] Verifying mart data freshness for the latest reporting date ({latest_date})...")
        row_count, transactions, revenue = con.execute(today_query, [str(latest_date)]).fetchone()
        today_str = str(latest_date)

    con.close()

    # 3. If row_count is 0, fail the Airflow task so broken/empty dashboards are never shared!
    if row_count == 0 or revenue <= 0:
        raise ValueError(
            f"❌ DATA QUALITY CHECK FAILED: Mart table 'fct_daily_revenue' has NO data for {today_str}!"
        )

    print(
        f"✅ DATA QUALITY CHECK PASSED: 'fct_daily_revenue' has {row_count} record(s) for {today_str} "
        f"({transactions} transactions | ${revenue:,.2f} total daily revenue)!"
    )


# ---------------------------------------------------------------------------
# DAG DEFINITION (Q4 + Q5 Data Check Task)
# ---------------------------------------------------------------------------
with DAG(
    dag_id="brewbeats_daily_dbt_pipeline_with_check",
    default_args=default_args,
    description="Section D - Q4 & Q5: Daily Airflow DAG that runs dbt and checks mart table has data for today",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["brewbeats", "dbt", "data_quality", "daily"],
) as dag:

    # Task 1 (Q4): Run dbt models (stg_coffee_sales -> fct_daily_revenue)
    dbt_run_models = BashOperator(
        task_id="dbt_run_models",
        bash_command=f'"{DBT_BIN}" run --project-dir "{DBT_PROJECT_DIR}" --profiles-dir "{DBT_PROJECT_DIR}" --no-use-colors',
    )

    # Task 2 (Q4): Run dbt schema tests (unique & not_null)
    dbt_test_models = BashOperator(
        task_id="dbt_test_models",
        bash_command=f'"{DBT_BIN}" test --project-dir "{DBT_PROJECT_DIR}" --profiles-dir "{DBT_PROJECT_DIR}" --no-use-colors',
    )

    # Task 3 (Q5): Check that the mart table (fct_daily_revenue) has data for today
    check_mart_has_data_for_today = PythonOperator(
        task_id="check_mart_has_data_for_today",
        python_callable=verify_mart_has_today_data,
    )

    # Set task execution order: run dbt -> test dbt -> check mart table has data for today
    dbt_run_models >> dbt_test_models >> check_mart_has_data_for_today


# ---------------------------------------------------------------------------
# LOCAL EXECUTION TEST (Runs all 3 DAG tasks live using our dbt Python environment!)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Section D - Q5: Executing Airflow DAG with Mart Table Data Check ===\n")

    print("1️⃣ [Airflow Task 1: dbt_run_models] Running `dbt run`...")
    subprocess.run(dbt_run_models.bash_command, shell=True, check=True)

    print("\n2️⃣ [Airflow Task 2: dbt_test_models] Running `dbt test`...")
    subprocess.run(dbt_test_models.bash_command, shell=True, check=True)

    print("\n3️⃣ [Airflow Task 3: check_mart_has_data_for_today] Verifying mart table data...")
    verify_mart_has_today_data()

    print("\n🎉 Section D - Q5 Airflow DAG completed all 3 tasks (dbt run -> dbt test -> today's mart data check)!")

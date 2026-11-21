"""
=============================================================================
BrewBeats — Mini Project 2: Section D (dbt + Airflow Pipeline)
Folder  : Section D - dbt + Airflow Pipeline/Section D_Q4/
File    : Section_D_Q4_airflow_dbt_dag.py
Task    : Section D - Q4: Create a simple Airflow DAG that runs the dbt project once a day.
Schedule: Once a day (@daily / 0 6 * * *)
=============================================================================
How this Airflow DAG works:
1. What is an Airflow DAG?
   A DAG (Directed Acyclic Graph) in Apache Airflow is an automated workflow scheduler.
   Instead of a data engineer running `dbt run` and `dbt test` manually every morning,
   Airflow runs the tasks automatically on a schedule (`schedule="@daily"`) and in the right order.
2. What tasks are inside this DAG?
   - Task 1 (`dbt_run_models`): Uses Airflow's `BashOperator` to run `dbt run`, which builds
     our staging view (`stg_coffee_sales`) and daily revenue mart table (`fct_daily_revenue`).
   - Task 2 (`dbt_test_models`): Uses `BashOperator` to run `dbt test`, which checks our
     `unique` and `not_null` data quality rules from `schema.yml`.
3. Task Dependency (`dbt_run_models >> dbt_test_models`):
   The `>>` operator tells Airflow that `dbt_run_models` must finish successfully first
   before `dbt_test_models` starts!
"""

from datetime import datetime, timedelta
import subprocess

# ---------------------------------------------------------------------------
# AIRFLOW IMPORTS (With graceful local fallback so we can also test it directly in terminal!)
# ---------------------------------------------------------------------------
try:
    from airflow import DAG
    from airflow.operators.bash import BashOperator
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

# Paths to our dbt executable and our BrewBeats dbt project folder (from Section D - Q1/Q2/Q3)
DBT_BIN = '/Users/rosi/Documents/IronHack Course /Week 06/Day 05 - Snowflake_DBT/dbt-env/bin/dbt'
DBT_PROJECT_DIR = '/Users/rosi/Documents/IronHack Course /Week 07/Day 03-04-05 - Mini Project 2/Section D - dbt + Airflow Pipeline/Section D_Q1/brewbeats_dbt'

# Default settings applied to all tasks in our DAG (owner, retries if a task fails, retry delay)
default_args = {
    "owner": "rosi_brewbeats_data_engineer",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# ---------------------------------------------------------------------------
# SECTION D - Q4: Define the Daily Airflow DAG
# ---------------------------------------------------------------------------
# - dag_id="brewbeats_daily_dbt_pipeline": unique name of our DAG in the Airflow UI
# - schedule="@daily": tells Airflow to run this pipeline automatically once a day
# - catchup=False: tells Airflow not to re-run past historical dates when first turned on
with DAG(
    dag_id="brewbeats_daily_dbt_pipeline",
    default_args=default_args,
    description="Section D - Q4: Simple Airflow DAG that runs the BrewBeats dbt project once a day",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["brewbeats", "dbt", "daily"],
) as dag:

    # Task 1: Run `dbt run` to build stg_coffee_sales (view) and fct_daily_revenue (table)
    dbt_run_models = BashOperator(
        task_id="dbt_run_models",
        bash_command=f'"{DBT_BIN}" run --project-dir "{DBT_PROJECT_DIR}" --profiles-dir "{DBT_PROJECT_DIR}" --no-use-colors',
    )

    # Task 2: Run `dbt test` to verify all unique and not_null tests pass
    dbt_test_models = BashOperator(
        task_id="dbt_test_models",
        bash_command=f'"{DBT_BIN}" test --project-dir "{DBT_PROJECT_DIR}" --profiles-dir "{DBT_PROJECT_DIR}" --no-use-colors',
    )

    # Set task execution order: run dbt models first, then test them
    dbt_run_models >> dbt_test_models


# ---------------------------------------------------------------------------
# LOCAL EXECUTION TEST (Runs both DAG tasks live and prints the output!)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Section D - Q4: Executing Airflow DAG 'brewbeats_daily_dbt_pipeline' (@daily) ===\n")

    print("1️⃣ [Airflow Task: dbt_run_models] Running `dbt run`...")
    subprocess.run(dbt_run_models.bash_command, shell=True, check=True)

    print("\n2️⃣ [Airflow Task: dbt_test_models] Running `dbt test`...")
    subprocess.run(dbt_test_models.bash_command, shell=True, check=True)

    print("\n✅ Section D - Q4 Airflow DAG completed all daily dbt tasks successfully!")

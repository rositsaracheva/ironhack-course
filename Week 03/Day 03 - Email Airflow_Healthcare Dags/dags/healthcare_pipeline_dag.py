from datetime import datetime, timedelta
import logging
import os
import pandas as pd
from airflow import DAG

# Compatible PythonOperator import
try:
    from airflow.operators.python import PythonOperator
except ImportError:
    from airflow.providers.standard.operators.python import PythonOperator

# File paths inside the Docker container
RAW_DATA_PATH = "/opt/airflow/data/raw/patient_vitals.csv"
PROCESSED_DATA_PATH = "/opt/airflow/data/processed/validated_vitals.csv"
REPORT_PATH = "/opt/airflow/data/reports/patient_daily_report.txt"

default_args = {
    "owner": "hospital_data_team",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


# -----------------------------------------------------------------------------
# TASK LOGIC FUNCTIONS
# -----------------------------------------------------------------------------

def collect_patient_vitals():
    """Task 1: Simulates collecting vitals from medical devices."""
    logging.info("Collecting patient vitals from medical monitors...")

    vitals_data = [
        {"patient_id": "P001", "heart_rate": 72, "systolic_bp": 120, "oxygen_level": 98},
        {"patient_id": "P002", "heart_rate": 88, "systolic_bp": 135, "oxygen_level": 96},
        {"patient_id": "P003", "heart_rate": 110, "systolic_bp": 145, "oxygen_level": 93},
        {"patient_id": "P004", "heart_rate": 65, "systolic_bp": 118, "oxygen_level": 99},
    ]

    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    df = pd.DataFrame(vitals_data)
    df.to_csv(RAW_DATA_PATH, index=False)
    logging.info("Collected %d patient records and saved to %s", len(df), RAW_DATA_PATH)


def validate_records():
    """Task 2: Validates records (error handling & sanity checks)."""
    logging.info("Validating patient vitals records...")

    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Raw file not found: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)

    # Sanity checks: heart rate and oxygen levels must be realistic
    if (df["heart_rate"] <= 0).any() or (df["heart_rate"] > 220).any():
        raise ValueError("Invalid heart rate detected in patient records!")

    if (df["oxygen_level"] < 50).any() or (df["oxygen_level"] > 100).any():
        raise ValueError("Invalid oxygen saturation percentage detected!")

    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    logging.info("All %d patient records successfully validated!", len(df))


def store_in_database():
    """Task 3: Simulates storing validated records into the database."""
    logging.info("Connecting to hospital database...")

    df = pd.read_csv(PROCESSED_DATA_PATH)
    # Simulate DB insert
    logging.info("Successfully inserted %d records into patient_records table.", len(df))


def generate_reports():
    """Task 4: Generates a daily clinical summary report."""
    logging.info("Generating daily patient summary report...")

    df = pd.read_csv(PROCESSED_DATA_PATH)
    avg_hr = df["heart_rate"].mean()
    high_bp_patients = df[df["systolic_bp"] >= 130]

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("=== HOSPITAL PATIENT DAILY MONITORING REPORT ===\n")
        f.write(f"Total Patients Monitored: {len(df)}\n")
        f.write(f"Average Heart Rate: {avg_hr:.1f} bpm\n")
        f.write(f"Patients with High Blood Pressure: {len(high_bp_patients)}\n")

    logging.info("Report saved to %s", REPORT_PATH)


# -----------------------------------------------------------------------------
# DAG DEFINITION (Satisfies all 5 Lab Questions)
# -----------------------------------------------------------------------------

with DAG(
    dag_id="healthcare_patient_pipeline",
    description="Automated pipeline for patient vitals collection, validation, and reporting",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",                        # Question 3: Daily schedule
    catchup=False,
    default_args=default_args,
    tags=["healthcare", "patient_data", "hospital"],  # Question 4: Healthcare tags
) as dag:

    # Question 1: Create four tasks
    task_collect = PythonOperator(
        task_id="collect_patient_vitals",
        python_callable=collect_patient_vitals,
    )

    task_validate = PythonOperator(
        task_id="validate_records",
        python_callable=validate_records,
    )

    task_store = PythonOperator(
        task_id="store_in_database",
        python_callable=store_in_database,
    )

    # Question 5: Create a report generation task
    task_report = PythonOperator(
        task_id="generate_reports",
        python_callable=generate_reports,
    )

    # Question 2: Add sequential dependencies
    task_collect >> task_validate >> task_store >> task_report

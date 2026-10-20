from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
import pandas as pd
import os

RAW_FILE = "/opt/airflow/data/raw/bank_transactions.csv"
PROCESSED_FILE = "/opt/airflow/data/processed/analyzed_transactions.csv"
REPORT_FILE = "/opt/airflow/data/reports/fraud_alerts.csv"

# List of trusted / regular operating countries
TRUSTED_COUNTRIES = ["Spain", "France", "Germany", "Portugal", "Italy"]

default_args = {
    "owner": "fraud_team",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


def analyze_fraud_transactions():
    """Reads the raw bank transactions CSV, flags fraudulent transactions

    based on business rules (amount > 5000 OR untrusted country),
    adds the 'fraud_detected' boolean column, and saves to processed file.
    """
    if not os.path.exists(RAW_FILE):
        raise FileNotFoundError(f"Raw file not found: {RAW_FILE}")

    df = pd.read_csv(RAW_FILE)

    # Fraud condition: either amount > 5000 OR country not in trusted list
    fraud_condition = (df["amount"] > 5000) | (~df["country"].isin(TRUSTED_COUNTRIES))

    # Add fraud_detected column (True if fraud, False otherwise)
    df["fraud_detected"] = fraud_condition

    # Ensure processed directory exists and save analyzed dataset
    os.makedirs(os.path.dirname(PROCESSED_FILE), exist_ok=True)
    df.to_csv(PROCESSED_FILE, index=False)

    print("=== TRANSACTION ANALYSIS COMPLETED ===")
    print(f"Total transactions analyzed: {len(df)}")
    print(f"Total frauds detected: {df['fraud_detected'].sum()}")


def generate_fraud_report():
    """Reads the analyzed transactions file, extracts flagged frauds,

    saves them to a dedicated report CSV, and logs the alert details.
    """
    if not os.path.exists(PROCESSED_FILE):
        raise FileNotFoundError(f"Processed file not found: {PROCESSED_FILE}")

    df = pd.read_csv(PROCESSED_FILE)
    frauds_df = df[df["fraud_detected"] == True]

    # Ensure reports directory exists and save alerts report
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    frauds_df.to_csv(REPORT_FILE, index=False)

    print("=== FRAUD REPORT GENERATION COMPLETED ===")
    print(f"Total fraudulent transactions in report: {len(frauds_df)}")

    if len(frauds_df) > 0:
        print("\n--- FRAUDULENT TRANSACTIONS DETAILS ---")
        for _, row in frauds_df.iterrows():
            print(
                f"[ALERT] ID: {row['transaction_id']} | "
                f"Amount: {row['amount']} EUR | "
                f"Country: {row['country']} | "
                f"Merchant: {row['merchant']} | "
                f"Timestamp: {row['timestamp']}"
            )


with DAG(
    dag_id="fraud_detection_pipeline",
    description="Hourly pipeline for bank transactions ingestion, fraud detection, and reporting",
    start_date=datetime(2026, 10, 1),
    schedule="@hourly",
    catchup=False,
    default_args=default_args,
    tags=["banking", "fraud_detection", "hourly"],
) as dag:

    # Task 1: Wait for raw bank_transactions.csv file
    wait_for_transactions_file = FileSensor(
        task_id="wait_for_transactions_file",
        filepath=RAW_FILE,
        poke_interval=30,
        timeout=300,
        mode="poke",
    )

    # Task 2: Analyze transactions and flag fraud (amount > 5000 OR untrusted country)
    detect_fraud_task = PythonOperator(
        task_id="detect_fraud_transactions",
        python_callable=analyze_fraud_transactions,
    )

    # Task 3: Read analyzed transactions and generate dedicated fraud report
    generate_report_task = PythonOperator(
        task_id="generate_fraud_report",
        python_callable=generate_fraud_report,
    )

    # Define task dependencies
    wait_for_transactions_file >> detect_fraud_task >> generate_report_task

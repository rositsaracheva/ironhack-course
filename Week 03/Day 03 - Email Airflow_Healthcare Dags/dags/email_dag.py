from datetime import datetime
import logging
from airflow import DAG

# Compatible PythonOperator import
try:
    from airflow.operators.python import PythonOperator
except ImportError:
    from airflow.providers.standard.operators.python import PythonOperator

from airflow.utils.email import send_email


def send_notification():
    logging.info("Starting email notification...")

    send_email(
        to=["rosisaracheva@gmail.com"],  # Sends the test email to your inbox
        subject="Airflow Email Notification Test - Success!",
        html_content="""
        <h2>Airflow Email Test</h2>
        <p>Hello Rosi!</p>
        <p>Your Airflow DAG ran successfully and sent this email automatically.</p>
        <p>Docker + Airflow + SMTP are working perfectly together!</p>
        """,
    )

    logging.info("Email notification sent successfully.")


with DAG(
    dag_id="email_dag",
    description="Send an email notification from Airflow",
    start_date=datetime(2026, 1, 1),
    schedule=None,  # Manual trigger for testing
    catchup=False,
    tags=["email", "notification"],
) as dag:

    email_task = PythonOperator(
        task_id="send_email",
        python_callable=send_notification,
    )

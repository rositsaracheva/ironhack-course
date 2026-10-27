FROM apache/airflow:latest

# Install dependencies including dbt-duckdb
COPY --chown=airflow:root requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

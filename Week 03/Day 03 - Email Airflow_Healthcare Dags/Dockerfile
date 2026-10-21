FROM apache/airflow:latest

# Instalar dependencias adicionales de Python (ej: pandas)
COPY --chown=airflow:root requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt
# ==============================================================================
# Dockerfile for Apache Airflow (Latest official version)
# ==============================================================================
FROM apache/airflow:latest

# Install basic OS utilities (as root)
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to the standard airflow user (UID: 50000) for security best practices
USER airflow

# Base Airflow configuration
ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW__WEBSERVER__WEB_SERVER_HOST=0.0.0.0

# Copy and install additional Python dependencies if defined in requirements.txt
COPY --chown=airflow:root requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Expose port for Web UI and REST API access
EXPOSE 8080

# Start Airflow in standalone mode (runs Webserver, Scheduler, and Triggerer in a single process)
CMD ["standalone"]

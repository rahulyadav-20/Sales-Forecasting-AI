ARG AIRFLOW_IMAGE=apache/airflow:3.2.1
FROM ${AIRFLOW_IMAGE}

USER root
RUN mkdir -p /usr/local/airflow/include \
    && chown -R airflow:0 /usr/local/airflow

USER airflow

# Install Python dependencies needed by the DAG code.
COPY requirements-airflow.txt /tmp/requirements-airflow.txt
RUN pip install --no-cache-dir -r /tmp/requirements-airflow.txt

# Bake DAGs and helper modules into the Airflow image.
COPY --chown=airflow:0 dags/ /opt/airflow/dags/
COPY --chown=airflow:0 include/ /opt/airflow/include/
COPY --chown=airflow:0 include/ /usr/local/airflow/include/

# Set environment variables for MLflow and MinIO
ENV MLFLOW_TRACKING_URI=http://mlflow:5001
ENV MLFLOW_S3_ENDPOINT_URL=http://minio:9000
ENV AWS_DEFAULT_REGION=us-east-1
ENV PYTHONPATH=/opt/airflow/include:/usr/local/airflow/include

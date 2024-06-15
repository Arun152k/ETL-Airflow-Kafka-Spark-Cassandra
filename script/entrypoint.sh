#!/bin/bash
set -e

if [ -e "/opt/airflow/requirements.txt" ]; then
  $(command python) pip install --upgrade pip
  $(command -v pip) install --user -r requirements.txt
fi

if [ ! -f "/opt/airflow/airflow.db" ]; then
  airflow db init && \
  airflow users create \
    --username {AIRFLOW_USERNAME} \
    --firstname {AIRFLOW_FIRST_NAME} \
    --lastname {AIRFLOW_LAST_NAME} \
    --role {AIRFLOW_ROLE} \
    --email {AIRFLOW_EMAIL} \
    --password {AIRFLOW_PASSWORD}
fi

$(command -v airflow) db upgrade

exec airflow webserver
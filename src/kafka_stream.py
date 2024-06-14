from datetime import datetime, timedelta
import uuid

from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import json
from kafka import KafkaProducer
import time
import logging


default_args = {
    "owner": "Arun Kumar",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 6, 2, 10, 30),
}


def get_data():

    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res["results"][0]
    return res


def format_data(res):

    data = {}
    location = res["location"]
    data["id"] = str(uuid.uuid4())
    data["first_name"] = res["name"]["first"]
    data["last_name"] = res["name"]["last"]
    data["gender"] = res["gender"]
    data["address"] = (
        f"{str(location['street']['number'])} {location['street']['name']}, "
        f"{location['city']}, {location['state']}, {location['country']}"
    )
    data["post_code"] = location["postcode"]
    data["email"] = res["email"]
    data["username"] = res["login"]["username"]
    data["dob"] = res["dob"]["date"]
    data["registered_date"] = res["registered"]["date"]
    data["phone"] = res["phone"]
    data["picture"] = res["picture"]["medium"]
    return data


def stream_data():

    producer = KafkaProducer(bootstrap_servers=["broker:29092"], max_block_ms=5000)
    curr_time = time.time()

    while True:
        if time.time() > curr_time + 10:
            break
        else:
            try:
                res = get_data()
                res = format_data(res)
                producer.send("user_stream", json.dumps(res).encode("utf-8"))
                logging.info(f"Message sent to the broker ....")
            except Exception as e:
                logging.error(f"Error occured when sending to the broker: {e}")


with DAG(
    dag_id="user_stream",
    default_args=default_args,
    schedule=timedelta(seconds=5),
    catchup=False,
) as dag:

    streaming_task = PythonOperator(
        task_id="stream_data_from_api", python_callable=stream_data
    )

streaming_task

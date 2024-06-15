# ETL and Streaming Data Pipeline

*** *Active Repository* ***

This repository contains a robust ETL pipeline with Change Data Capture (CDC) using Airflow, Kafka, Spark, Cassandra and Debezium, and a Flask API with Swagger documentation. The pipeline efficiently extracts data from an external API, transforms it, and loads it to database sink. Additionally, it incorporates Change-Data-Capture (CDC) using Debezium and Kafka Connect to track and stream changes from a PostgreSQL database, ensuring real-time data synchronization.

Screenshots demonstrating the functionality of the various tools in the pipeline are available in the [images](images) folder.

Huge shout out to [AirScholar](https://www.youtube.com/watch?v=GqAcTrqKcrY) video.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Components](#components)
- [Endpoints](#endpoints)
- [Change Data Capture (CDC)](#Change-Data-Capture)

## Project Overview

This project implements a comprehensive ETL and streaming data pipeline. The pipeline begins by fetching random user data from an external API and streaming it to Kafka. Spark then consumes the Kafka stream, processes the data, and stores it in Cassandra. Airflow orchestrates the workflow, ensuring periodic API calls to fetch data. Additionally, a Flask API with Swagger documentation is provided to interact with the transformed data loaded in Cassandra, offering endpoints for various CRUD operations. 

Additionally, a Change Data Capture (CDC) proof of concept using Debezium and Kafka Connect was implemented. This setup captures changes in a PostgreSQL database and streams them to Kafka.

Random user data is fetched from an external API ([randomuser.me](https://randomuser.me)) and processed through the pipeline to simulate real-world scenarios.

## Architecture

- **Kafka**: Used for streaming data.
- **Spark**: Processes and transforms the data from Kafka.
- **Cassandra**: Stores the transformed data.
- **Airflow**: Orchestrates the ETL process.
- **Flask**: Provides API endpoints to interact with the Cassandra data.
- **Swagger**: Documents the API endpoints.
- **Debezium**: Captures changes in the PostgreSQL database and streams them to Kafka.
- **Kafka Connect**: Uses the Debezium Postgres connector to manage the data capture process.

## Docker Containers

- **Zookeeper**: Manages and coordinates the Kafka brokers.
- **Kafka Broker**: Handles the data streaming and messaging.
- **Schema Registry**: Manages and provides access to Avro schemas for Kafka messages.
- **Control Center**: Provides a web-based interface to monitor and manage the Kafka ecosystem.
- **Airflow Webserver and Scheduler**: Orchestrates the ETL workflow with task scheduling and execution.
- **PostgreSQL**: Serves as the source database for the Change Data Capture (CDC) process. Airflow's metadata is also stored here.
- **Spark Master and Worker**: Executes the data processing tasks.
- **Cassandra**: Stores the processed data.
- **Debezium**: Captures changes in the PostgreSQL database and streams them to Kafka.
- **Kafka Connect UI**: Provides a user interface to manage and monitor Kafka Connect.

## Getting Started
 
1. Clone the repository

   ```git clone https://github.com/your-rep etl-streaming-pipeline.git```

2. Set up the environment variables in a .env file

    ``` POSTGRES_USER="your_postgres_user"
    POSTGRES_PASSWORD="your_postgres_password"
    POSTGRES_DB="your_postgres_db"
    CASSANDRA_USERNAME="your_cassandra_username"
    CASSANDRA_PASSWORD="your_cassandra_password"
    AIRFLOW_USERNAME="your_airflow_username"
    AIRFLOW_FIRST_NAME="your_airflow_first_name"
    AIRFLOW_LAST_NAME="your_airflow_last_name"
    AIRFLOW_ROLE="your_airflow_role"
    AIRFLOW_EMAIL="your_airflow_email"
    AIRFLOW_PASSWORD="your_airflow_password"
    ```

2. Start the services using Docker Compose

    ```docker-compose up -d```

3. Install the requirements

    ```pip install -r requirements.txt```

4. Run kafka_stream.py to set up airflow and produce messages into Kafka

    ```python3 kafka_stream.py```

5. Run the ETL pipeline

    ```python3 ETL.py```

6. Run the Flask to set up API endpoints for accessing Cassandra

    ```python3 flaskServer.py```

7. Vist ```http://127.0.0.1:5000/apidocs/``` for the API endpoints

# Important Components

### `kakfa_stream.py`
Defines an Airflow DAG that fetches random user data from an external API, formats it, and streams it to Kafka.

### `ETL.py`
Contains the ETL pipeline using Spark to consume data from Kafka, process it, and store it in Cassandra.

### `flaskServer.py`
Provides API endpoints using Flask and Swagger to interact with the data stored in Cassandra. Endpoints include fetching the first five rows, counting rows, adding, updating, deleting, and searching for users.

### `docker-compose.yml`
Defines the Docker services required for the pipeline, including Kafka, Zookeeper, Schema Registry, Airflow, Spark, Cassandra, and Debezium for change data capture.

### `script/entrypoint.sh`
A script to initialize Airflow, install requirements, and set up the Airflow database.

# Change-Data-Capture

Debezium is used to capture changes in the PostgreSQL database and stream them to Kafka. Kafka Connect is configured to use the Debezium Postgres connector.

The [postgres-connector.json](postgres-connector.json) file defines the configuration for the Debezium Postgres connector, specifying the database connection details and the Kafka topics for streaming the changes.

Debezium and Kafka Connect should already be set up when you run `docker-compose`.

Configure Debezium using:

```curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d @postgres-connector.json```


## CDC at play:

The earlier ETL pipleline loads into Cassandra. For CDC, a PostgreSQL database was used.

The CDC messages in Kafka can be viewed here [CDCMessages](debezium/messages_postgresDebesium.public.created_users.csv).
A comprehensive POC with images can be viewed in [DebeziumPOC](debezium/DebeziumPOC.pdf).

## Summary

In this project, a robust ETL pipeline was built, that integrates multiple technologies to fetch, process, and store user data. We utilized Airflow to orchestrate the workflow, Kafka for streaming the data, and Spark for processing the data. The processed data is then stored in Cassandra. Additionally, we implemented Debezium and Kafka Connect for change data capture from a PostgreSQL database, ensuring that any changes in the source database are streamed to Kafka in real-time. A Flask API with Swagger documentation was provided to interact with the stored data, offering endpoints for various CUD operations.
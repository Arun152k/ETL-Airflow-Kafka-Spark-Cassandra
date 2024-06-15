# ETL and Streaming Data Pipeline

*** *Active Repository* ***

This repository showcases a robust ETL and streaming data pipeline leveraging Kafka, Spark, Airflow, Cassandra, and a Flask API with Swagger documentation. The pipeline efficiently fetches data from an external API, processes it, and streams it to various services for storage and further processing. Additionally, it incorporates Change-Data-Capture (CDC) using Debezium and Kafka Connect to track and stream changes from a PostgreSQL database, ensuring real-time data synchronization.

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

This project implements a comprehensive ETL and streaming data pipeline. The pipeline begins by fetching random user data from an external API and streaming it to Kafka. Spark then consumes the Kafka stream, processes the data, and stores it in Cassandra. Airflow orchestrates the entire workflow, ensuring seamless data flow and processing. Additionally, a Flask API with Swagger documentation is provided to interact with the data stored in Cassandra, offering endpoints for various CRUD operations. For real-time data synchronization, I implemented a CDC proof of concept using Debezium and Kafka Connect to capture changes in a PostgreSQL database and stream them to Kafka.

## Architecture

- **Kafka**: Used for streaming data.
- **Spark**: Processes and transforms the data from Kafka.
- **Cassandra**: Stores the processed data.
- **Airflow**: Orchestrates the ETL process.
- **Flask**: Provides API endpoints to interact with the stored data.
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
 
1. **Clone the repository:**

   ```git clone https://github.com/your-rep etl-streaming-pipeline.git```

2. Set up the environment variables in a .env file

2. Start the services using Docker Compose:

    ```docker-compose up -d```

3. Install the requirements

    ```pip install -r requirements.txt```

4. Run kafka_stream.py to set up airflow and produce messages into Kafka

    ```python3 kafka_stream.py```

5. Run the ETL pipeline

    ```python3 ETL.py```

6. Run the Flask to set up API endpoints for accessing Cassandra.

    ```python3 flaskServer.py```

7. Vist ```http://127.0.0.1:5000/apidocs/``` for the API endpoints

# Components

### `kakfa_stream.py`
Defines an Airflow DAG that fetches random user data from an external API, formats it, and streams it to Kafka.

### `ETL.py`
Contains the ETL logic using Spark to consume data from Kafka, process it, and store it in Cassandra. It also defines functions to create keyspace and tables in Cassandra.

### `flaskServer.py`
Provides API endpoints using Flask and Swagger to interact with the data stored in Cassandra. Endpoints include fetching the first five rows, counting rows, adding, updating, deleting, and searching for users.

### `docker-compose.yml`
Defines the Docker services required for the pipeline, including Kafka, Zookeeper, Schema Registry, Airflow, Spark, Cassandra, and Debezium for change data capture.

### `script/entrypoint.sh`
A script to initialize Airflow, install requirements, and set up the Airflow database.

# Endpoints

### `/count`
- **Method**: GET
- **Description**: Returns the number of rows in the `created_users` table.

### `/first-five`
- **Method**: GET
- **Description**: Returns the first five rows from the `created_users` table.

### `/add-user`
- **Method**: POST
- **Description**: Adds a new user to the `created_users` table.

### `/update-user/<user_id>`
- **Method**: PUT
- **Description**: Updates an existing user in the `created_users` table.

### `/delete-user/<user_id>`
- **Method**: DELETE
- **Description**: Deletes a user from the `created_users` table.

### `/get-user/<user_id>`
- **Method**: GET
- **Description**: Retrieves a user by ID from the `created_users` table.

### `/search-user`
- **Method**: GET
- **Description**: Searches users by first name in the `created_users` table.

# Change-Data-Capture

Debezium is used to capture changes in the PostgreSQL database and stream them to Kafka. Kafka Connect is configured to use the Debezium Postgres connector.

The postgres-connector.json file defines the configuration for the Debezium Postgres connector, specifying the database connection details and the Kafka topics for streaming the changes.

Debezium and Kafka Connect should already been set up when you run docker-compose. 

Configure Debezium using:

```curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d @postgres-connector.json```


# Change-Data-Capture

Debezium is used to capture changes in the PostgreSQL database and stream them to Kafka. Kafka Connect is configured to use the Debezium Postgres connector.

The [postgres-connector.json](postgres-connector.json) file defines the configuration for the Debezium Postgres connector, specifying the database connection details and the Kafka topics for streaming the changes.

Debezium and Kafka Connect should already be set up when you run `docker-compose`.

Configure Debezium using:

```curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d @postgres-connector.json```


## CDC at play:

The earlier ETL pipleline loads into Cassandra. For CDC, I have used a PostgreSQL database.

The workflow with images can be viewed in [DebeziumPOC](debezium/DebeziumPOC.pdf).

The CDC messages in Kafka can be viewed here [CDCMessages](debezium/messages_postgresDebesium.public.created_users.csv).
The workflow with images can be viewed in [DebeziumPOC](debezium/DebeziumPOC.pdf).

The CDC messages in Kafka can be viewed here [CDCMessages](debezium/messages_postgresDebesium.public.created_users.csv).


## Summary

In this project, we built a robust ETL and streaming data pipeline that integrates multiple technologies to fetch, process, and store user data efficiently. We utilized Airflow to orchestrate the workflow, Kafka for streaming the data, and Spark for processing the data. The processed data is then stored in Cassandra for persistence. Additionally, we implemented Debezium and Kafka Connect for change data capture from a PostgreSQL database, ensuring that any changes in the source database are streamed to Kafka in real-time. A Flask API with Swagger documentation was provided to interact with the stored data, offering endpoints for various CUD operations.
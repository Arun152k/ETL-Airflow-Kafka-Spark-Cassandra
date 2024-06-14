import findspark

findspark.init()
findspark.find()

import logging

from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_keyspace(session):
    session.execute(
        """CREATE KEYSPACE IF NOT EXISTS spark_streams
                        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
                    """
    )
    logger.info(f"Keyspace Created!")


def create_table(session):
    session.execute(
        """CREATE TABLE IF NOT EXISTS spark_streams.user_stream(
                    id TEXT PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    gender TEXT,
                    dob TEXT,
                    address TEXT,
                    post_code TEXT,
                    email TEXT,
                    username TEXT,
                    registered_date TEXT,
                    phone TEXT,
                    picture TEXT
    );
                    """
    )
    logger.info(f"Table Created!")


def create_spark_connection():
    s_conn = None
    try:
        s_conn = (
            SparkSession.builder.appName("SparkDataStreaming")
            .config(
                "spark.jars.packages",
                "com.datastax.spark:spark-cassandra-connector_2.12:3.1.0,"
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.0",
            )
            .config("spark.cassandra.connection.host", "localhost")
            .getOrCreate()
        )
        s_conn.sparkContext.setLogLevel("ERROR")
        logger.info(f"Spark session created successfully.")

    except Exception as e:
        logger.error(f"Error creating Spark session: {e}")

    return s_conn


def create_cassandra_connection():
    session = None
    try:
        cluster = Cluster(["localhost"])
        session = cluster.connect()
        logging.info(f"Cassandra Connected")
    except Exception as e:
        logger.error(f"Error creating Cassandra session: {e}")

    return session


def connect_to_kafka(spark_conn):

    spark_df = None

    try:
        spark_df = (
            spark_conn.readStream.format("kafka")
            .option("kafka.bootstrap.servers", "localhost:9092")
            .option("subscribe", "users_created")
            .option("startingOffsets", "earliest")
            .load()
        )
        logging.info(f"Succesfully created the initial Kafka Dataframe")

    except Exception as e:
        logging.error(f"Error in creating the initial DataFrame: {e}")

    return spark_df


def create_selection_df_from_kafka(spark_df):
    schema = StructType(
        [
            StructField("id", StringType(), False),
            StructField("first_name", StringType(), False),
            StructField("last_name", StringType(), False),
            StructField("dob", StringType(), False),
            StructField("gender", StringType(), False),
            StructField("address", StringType(), False),
            StructField("post_code", StringType(), False),
            StructField("email", StringType(), False),
            StructField("username", StringType(), False),
            StructField("registered_date", StringType(), False),
            StructField("phone", StringType(), False),
            StructField("picture", StringType(), False),
        ]
    )
    sel = (
        spark_df.selectExpr("CAST(value AS string)")
        .select(from_json(col("value"), schema).alias("data"))
        .select("data.*")
    )
    return sel


if __name__ == "__main__":
    spark_conn = create_spark_connection()
    if spark_conn is not None:

        spark_df = connect_to_kafka(spark_conn)
        selection_df = create_selection_df_from_kafka(spark_df)
        session = create_cassandra_connection()
        if session is not None:
            create_keyspace(session)
            create_table(session)
            streaming_query = (
                selection_df.writeStream.format("org.apache.spark.sql.cassandra")
                .option("checkpointLocation", "/tmp/checkpoint")
                .option("keyspace", "spark_streams")
                .option("table", "user_stream")
                .start()
            )
            streaming_query.awaitTermination()

        else:
            logger.warn(f"Cassandra Session is None")

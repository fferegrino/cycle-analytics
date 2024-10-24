import csv
import os
import time

import mysql.connector
from confluent_kafka.admin import AdminClient, NewTopic
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()


def setup_kafka_topics():
    kafka_admin = AdminClient({"bootstrap.servers": os.environ["KAFKA_BROKER"]})

    kafka_topics = {
        os.environ["DOCK_STATUS_UPDATE_TOPIC"]: {"num_partitions": 1, "replication_factor": 1, "config": {"retention.ms": "1800"}},
        os.environ["WEATHER_UPDATE_TOPIC"]: {"num_partitions": 1, "replication_factor": 1, "config": {"retention.ms": "1800"}},
    }

    for topic_name, config in kafka_topics.items():
        new_topic = NewTopic(topic_name, **config)

        existing_topics = kafka_admin.list_topics().topics
        if topic_name in existing_topics:
            print(f"Topic {topic_name} already exists, deleting it.")
            kafka_admin.delete_topics([topic_name])
            time.sleep(1)

        print(f"Creating topic {topic_name}")
        kafka_admin.create_topics([new_topic])


def setup_mysql_database():

    # MySQL configuration
    db_config = {
        "host": os.environ.get("MYSQL_HOST", "localhost"),
        "user": os.environ.get("MYSQL_USER"),
        "password": os.environ.get("MYSQL_PASSWORD"),
        "database": os.environ.get("MYSQL_DATABASE", "bike_sharing"),
    }

    connection = None

    try:
        connection = mysql.connector.connect(
            host=db_config.get("host", "localhost"), user=db_config.get("user"), password=db_config.get("password")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            db_name = db_config.get("database", "default_db")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"Database '{db_name}' created successfully.")

            connection.database = db_name

            create_table_query = """CREATE TABLE IF NOT EXISTS bike_stations (
                place_id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                latitude DECIMAL(10, 8) NOT NULL,
                longitude DECIMAL(11, 8) NOT NULL
            );"""

            cursor.execute(create_table_query)
            print(f"Table 'bike_stations' created successfully.")

            with open("stations.csv", newline="") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row
                for row in reader:
                    cursor.execute(
                        "INSERT INTO bike_stations (place_id, name, latitude, longitude) VALUES (%s, %s, %s, %s)",
                        (row[0], row[5], float(row[3]), float(row[4])),
                    )
                connection.commit()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


if __name__ == "__main__":

    # Setup Kafka topics
    setup_kafka_topics()

    # Setup MySQL database and tables
    setup_mysql_database()

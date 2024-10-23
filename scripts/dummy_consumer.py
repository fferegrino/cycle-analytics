import os

from confluent_kafka import Consumer
from dotenv import load_dotenv

load_dotenv()

consumer = Consumer(
    {
        "bootstrap.servers": os.environ["KAFKA_BROKER"],
        "group.id": "station-status-consumer",
        "auto.offset.reset": "earliest",
    }
)

consumer.subscribe([os.environ["DOCK_SATUS_UPDATE_TOPIC"]])

while True:
    message = consumer.poll(1.0)
    if message is None:
        continue
    if message.error() is not None:
        continue

    value = message.value().decode("utf-8")

    print(value)

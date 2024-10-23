import os
import time

from confluent_kafka.admin import AdminClient, NewTopic
from dotenv import load_dotenv

load_dotenv()

kafka_admin = AdminClient({"bootstrap.servers": os.environ["KAFKA_BROKER"]})

dock_updates_topic = NewTopic(os.environ["DOCK_SATUS_UPDATE_TOPIC"], num_partitions=1, replication_factor=1)


for topic in kafka_admin.list_topics().topics.values():
    if topic.topic == dock_updates_topic.topic:
        print(f"Topic {dock_updates_topic.topic} already exists, deleting it.")
        kafka_admin.delete_topics([dock_updates_topic.topic])
        time.sleep(1)

print(f"Creating topic {dock_updates_topic.topic}")
kafka_admin.create_topics([dock_updates_topic])

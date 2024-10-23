import csv
import json
import os
import random
import time
from datetime import datetime

from confluent_kafka import Producer
from dotenv import load_dotenv

random.seed(0)

load_dotenv()

with open("stations.csv", "r") as file:
    reader = csv.reader(file)
    headers = next(reader)
    stations = list(reader)

station_total_docks = {station[0]: int(station[1]) for station in stations}

station_available_docks = {station[0]: int(station[1]) - int(station[2]) for station in stations}

stations = list(station_total_docks.keys())


producer = Producer({"bootstrap.servers": os.environ["KAFKA_BROKER"]})


while True:
    station = random.choice(stations)
    available_docks = station_available_docks[station]
    action_random = random.random()

    message = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "station_id": station,
    }

    if action_random < 0.5:
        if station_available_docks[station] < station_total_docks[station]:
            station_available_docks[station] += 1
            print(
                f"{datetime.now()} - Station {station} docked a bike. Available docks: {station_available_docks[station]}"
            )
            message["action"] = "dock"
            message["available_docks"] = station_available_docks[station]
        else:
            print(f"{datetime.now()} - Station {station} is full. No bike docked.")
    else:
        if station_available_docks[station] > 0:
            station_available_docks[station] -= 1
            print(
                f"{datetime.now()} - Station {station} undocked a bike. Available docks: {station_available_docks[station]}"
            )
            message["action"] = "undock"
            message["available_docks"] = station_available_docks[station]
        else:
            print(f"{datetime.now()} - Station {station} is empty. No bike undocked.")

    if "action" in message:
        producer.produce(os.environ["DOCK_SATUS_UPDATE_TOPIC"], value=json.dumps(message))
        producer.poll()
    time.sleep(random.randint(0, 2))

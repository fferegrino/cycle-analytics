import csv
import decimal
import json
import os
import random
import time
from datetime import datetime

import numpy as np
from confluent_kafka import Producer
from dotenv import load_dotenv

random.seed(0)

load_dotenv()

WAIT_TIME = 10

latitudes = []
longitudes = []


def round_side(value, decimals, side):
    with decimal.localcontext() as ctx:
        d = decimal.Decimal(value)
        ctx.rounding = side
        return float(round(d, decimals))


with open("stations.csv", "r") as file:
    reader = csv.reader(file)
    headers = next(reader)
    for row in reader:
        latitudes.append(float(row[3]))
        longitudes.append(float(row[4]))

longitudes = np.array(longitudes)
latitudes = np.array(latitudes)

min_longitude = min(longitudes)
max_longitude = max(longitudes)
min_latitude = min(latitudes)
max_latitude = max(latitudes)

round_down_min_longitude = round_side(min_longitude, 2, decimal.ROUND_DOWN)
round_down_min_latitude = round_side(min_latitude, 2, decimal.ROUND_DOWN)
round_up_max_longitude = round_side(max_longitude, 2, decimal.ROUND_UP)
round_up_max_latitude = round_side(max_latitude, 2, decimal.ROUND_UP)

print(min_longitude, min_latitude)
print(round_down_min_longitude, round_down_min_latitude)

print(max_longitude, max_latitude)
print(round_up_max_longitude, round_up_max_latitude)

mapped_longitudes = np.arange(round_down_min_longitude - 0.01, round_up_max_longitude + 0.01, 0.01)
mapped_latitudes = np.arange(round_down_min_latitude - 0.01, round_up_max_latitude + 0.01, 0.01)


producer = Producer({"bootstrap.servers": os.environ["KAFKA_BROKER"]})


while True:
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    for lat in mapped_latitudes:
        for lon in mapped_longitudes:
            measurement = {
                "latitude": round(float(lat), 2),
                "longitude": round(float(lon), 2),
                "temperature": random.randint(-10, 40),
                "humidity": random.randint(0, 100),
                "timestamp": update_time,
            }
            producer.produce(os.environ['WEATHER_UPDATE_TOPIC'], json.dumps(measurement))
    print(f"Sent weather data at {update_time}")
    producer.poll()
    time.sleep(WAIT_TIME)

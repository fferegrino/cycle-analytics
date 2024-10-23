# Cycle analytics

## Setup

### 1. Setup containers

```
docker compose up --build -d
```

### 2. Setup the database and tables

This will create the Kafka topics and the database tables.

```
python scripts/setup.py
```

### 3. Start producing dock events

```
python scripts/events_simulator.py
```

#### 3.1 Verify events are being sent (optional)

```
python scripts/dummy_consumer.py
```

### 4. Start the Flink SQL client

```
docker compose run flink-sql-client
```

### 5. Create the tables

#### 5.1 Create the `dock_status_update` table

This table will "store" the events from the `dock_status_update` topic.

```sql
CREATE TABLE dock_status_update (
  `station_id` STRING,
  `action` STRING,
  `available_docks` INT,
  `timestamp` TIMESTAMP(3),
  WATERMARK FOR `timestamp` AS `timestamp` - INTERVAL '5' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'dock_status_update',
  'properties.group.id' = 'flink-group-1',
  'scan.startup.mode' = 'earliest-offset',
  'properties.bootstrap.servers' = 'broker:29092',
  'value.format' = 'json',
  'sink.partitioner' = 'fixed'
);

```

#### 5.2 Create the `bike_stations` table

This table will store the bike stations data.

```sql
CREATE TABLE bike_stations (
    place_id STRING,
    `name` STRING,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(10, 8),
    PRIMARY KEY (place_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://mysql:3306/bike_sharing?useSSL=false',
    'table-name' = 'bike_stations',
    'username' = 'root',
    'password' = 'root'
);
```

#### 5.3 Verify the tables are created (optional)

```sql
SHOW TABLES;
```

Now you can see the data being "streamed" into the table by running:

```sql
SELECT * FROM dock_status_update;
```

And the bike stations data by running:

```sql
SELECT * FROM bike_stations;
```

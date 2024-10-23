# Cycle analytics

## Setup

### 1. Setup containers

```
docker compose up --build -d
```

### 2. Setup Kafka infra

```
python scripts/setup_topic.py
```

### 3. Start producing events

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

### 5. Create the input table

```sql
CREATE TABLE dock_status_update (
  `station_id` STRING,
  `action` STRING,
  `timestamp` TIMESTAMP(3)
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

#### 5.1 Verify the table is created

```sql
SHOW TABLES;
```

Now you can see the data being "streamed" into the table by running:

```sql
SELECT * FROM dock_status_update;
```

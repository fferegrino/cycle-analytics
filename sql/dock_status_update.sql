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

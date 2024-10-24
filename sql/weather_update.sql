CREATE TABLE weather_update (
  `latitude` DOUBLE,
  `longitude` DOUBLE,
  `temperature` INT,
  `humidity` INT,
  `timestamp` TIMESTAMP(3),
  WATERMARK FOR `timestamp` AS `timestamp` - INTERVAL '1' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'weather_update',
  'properties.group.id' = 'flink-group-1',
  'scan.startup.mode' = 'earliest-offset',
  'properties.bootstrap.servers' = 'broker:29092',
  'value.format' = 'json',
  'sink.partitioner' = 'fixed'
);

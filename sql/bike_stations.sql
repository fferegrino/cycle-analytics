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

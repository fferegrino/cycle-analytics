SELECT
    a.station_id,
    b.latitude,
    b.longitude,
    a.average_available_docks,
    a.window_start,
    a.window_end
FROM (
    SELECT 
        station_id, 
        window_start, 
        window_end, 
        AVG(available_docks) AS average_available_docks 
    FROM 
    TABLE(
        TUMBLE(
        TABLE dock_status_update, 
        DESCRIPTOR(`timestamp`), 
        INTERVAL '1' MINUTES
        )
    ) 
    GROUP BY 
    station_id, 
    window_start, 
    window_end
) a
JOIN bike_stations b ON a.station_id = b.place_id;
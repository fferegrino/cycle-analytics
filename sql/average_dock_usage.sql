SELECT
    station_id,
    window_start,
    window_end,
    AVG(available_docks) AS average_available_docks
FROM TABLE(
    TUMBLE(TABLE dock_status_update, DESCRIPTOR(`timestamp`), INTERVAL '1' MINUTES))
GROUP BY station_id, window_start, window_end;

-- Tabela stacji
CREATE TABLE stations (
    station_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_name TEXT NOT NULL
);

-- Tabela wypożyczeń
CREATE TABLE rentals (
    rental_id TEXT PRIMARY KEY,
    bike_number TEXT NOT NULL,
    start_time DATETIME,
    end_time DATETIME,
    duration INTEGER,
    rental_station INTEGER,
    return_station INTEGER,
    FOREIGN KEY (rental_station) REFERENCES stations(station_id),
    FOREIGN KEY (return_station) REFERENCES stations(station_id)
);

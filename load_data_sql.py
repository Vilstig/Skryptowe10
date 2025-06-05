import csv
import os
import sys
import sqlite3
from datetime import datetime


def parse_datetime(dt_str): #move to db_utils
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S").isoformat()
    except Exception:
        return None


def get_or_create_station(conn, name):
    if name.lower() == "poza stacją" or not name.strip():
        return None
    cur = conn.cursor()
    cur.execute("SELECT station_id FROM stations WHERE station_name = ?", (name,))
    result = cur.fetchone()
    if result:
        return result[0]
    cur.execute("INSERT INTO stations (station_name) VALUES (?)", (name,))
    conn.commit()
    return cur.lastrowid


def load_csv_to_db(csv_path, db_path):
    conn = sqlite3.connect(f"{db_path}.sqlite3")
    conn.row_factory = sqlite3.Row

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader: #maybe move extracting the values to db_utils? the function could return all the vars as a tuple, then wed assign them to vars here. We could even use the ready tuple in the sql code
            rental_id = row["UID wynajmu"]
            bike_number = row["Numer roweru"]
            start_time = parse_datetime(row["Data wynajmu"])
            end_time = parse_datetime(row["Data zwrotu"])
            duration = int(row["Czas trwania"]) if row["Czas trwania"].isdigit() else None

            start_station_name = row["Stacja wynajmu"]
            end_station_name = row["Stacja zwrotu"]

            start_station_id = get_or_create_station(conn, start_station_name)
            end_station_id = get_or_create_station(conn, end_station_name)

            try:
                conn.execute("""
                    INSERT OR REPLACE INTO rentals (
                        rental_id, bike_number, start_time, end_time,
                        duration, rental_station, return_station
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    rental_id, bike_number, start_time, end_time,
                    duration, start_station_id, end_station_id
                ))
            except Exception as e:
                print(f"Błąd przy dodawaniu wiersza {rental_id}: {e}")

    conn.commit()
    conn.close()
    print(f"Załadowano dane z {csv_path} do bazy {db_path}.sqlite3")

def load_all(directory='data', db='rentals_sql'): #move to db_utils
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            load_csv_to_db(os.path.join(directory, file), db)

if __name__ == "__main__":
    '''if len(sys.argv) != 3:
        print("Użycie: python load_data.py <plik_csv> <nazwa_bazy>")
        sys.exit(1)

    csv_file = sys.argv[1]
    db_name = sys.argv[2]
    load_csv_to_db(csv_file, db_name)'''

    load_all()

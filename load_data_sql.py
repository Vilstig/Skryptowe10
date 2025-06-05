import csv
import sqlite3
from db_utils import parse_row, load_all


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

        for row in reader:
            try:
                conn.execute("""
                    INSERT OR REPLACE INTO rentals (
                        rental_id, bike_number, start_time, end_time,
                        duration, rental_station, return_station
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                parse_row(row, conn, get_or_create_station))
            except Exception as e:
                print(f"Błąd przy dodawaniu wiersza {row['UID wynajmu']}: {e}")

    conn.commit()
    conn.close()
    print(f"Załadowano dane z {csv_path} do bazy {db_path}.sqlite3")

if __name__ == "__main__":
    '''if len(sys.argv) != 3:
        print("Użycie: python load_data.py <plik_csv> <nazwa_bazy>")
        sys.exit(1)

    csv_file = sys.argv[1]
    db_name = sys.argv[2]
    load_csv_to_db(csv_file, db_name)'''

    load_all(directory='data', db='rentals_sql', load_func=load_csv_to_db)

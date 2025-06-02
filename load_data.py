import csv
import os
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Station, Rental


def load_csv_to_db(csv_path, db_path):
    # Połączenie z bazą danych
    engine = create_engine(f"sqlite:///{db_path}.sqlite3")
    Session = sessionmaker(bind=engine)
    session = Session()

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rental_id = row["UID wynajmu"]
            bike_number = row["Numer roweru"]
            start_time = parse_datetime(row["Data wynajmu"])
            end_time = parse_datetime(row["Data zwrotu"])
            duration = row['Czas trwania']

            start_station_name = row["Stacja wynajmu"]
            end_station_name = row["Stacja zwrotu"]

            start_station = get_or_create_station(session, start_station_name)
            end_station = get_or_create_station(session, end_station_name)

            rental = Rental(
                rental_id=rental_id,
                bike_number=bike_number,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                rental_station=start_station.station_id if start_station else None,
                return_station=end_station.station_id if end_station else None,
            )

            session.merge(rental)
        session.commit()
        session.close()
        print(f"Dane z {csv_path} załadowane do bazy {db_path}.sqlite3")


def get_or_create_station(session, name):
    if name.lower() == "poza stacją" or not name.strip():
        return None
    station = session.query(Station).filter_by(station_name=name).first()
    if not station:
        station = Station(station_name=name)
        session.add(station)
        session.commit()
    return station


def parse_datetime(dt_str):
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def load_all(directory='data', db='rentals'):
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            load_csv_to_db(os.path.join(directory, file), db)


if __name__ == "__main__":
    '''if len(sys.argv) != 3:
        print("Usage: python load_data.py <file_name> <database_name>")
        sys.exit(1)

    csv_file = sys.argv[1]
    db_name = sys.argv[2]
    load_csv_to_db(csv_file, db_name)'''

    load_all()

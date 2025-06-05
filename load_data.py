import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Station, Rental
from db_utils import parse_row, load_all


def load_csv_to_db(csv_path, db_path):
    # Połączenie z bazą danych
    engine = create_engine(f"sqlite:///{db_path}.sqlite3")
    Session = sessionmaker(bind=engine)
    session = Session()

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rental_id, bike_number, start_time, end_time, duration, start_station, end_station = parse_row(row, session, get_or_create_station)

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

def load_one(directory='data', db='rentals'): # DESTINED FOR TESTING
    i=0
    for file in os.listdir(directory):
        if i > 0:
            break
        i+=1
        if file.endswith(".csv"):
            load_csv_to_db(os.path.join(directory, file), db)

if __name__ == "__main__":
    '''if len(sys.argv) != 3:
        print("Usage: python load_data.py <file_name> <database_name>")
        sys.exit(1)

    csv_file = sys.argv[1]
    db_name = sys.argv[2]
    load_csv_to_db(csv_file, db_name)'''

    load_all(directory='data', db='rentals', load_func=load_csv_to_db)
    #load_one()
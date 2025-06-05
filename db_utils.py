from datetime import datetime
import os

def parse_datetime(dt_str): #move to db_utils
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None

def parse_row(row, session, station_func):
    return (row["UID wynajmu"],
            row["Numer roweru"],
            parse_datetime(row["Data wynajmu"]),
            parse_datetime(row["Data zwrotu"]),
            int(row["Czas trwania"]) if row["Czas trwania"].isdigit() else None,
            station_func(session, row["Stacja wynajmu"]),
            station_func(session, row["Stacja zwrotu"])
            )

def load_all(directory, db, load_func):
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            load_func(os.path.join(directory, file), db)
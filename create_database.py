import sys
from sqlalchemy import create_engine
from models import Base

def main():
    if len(sys.argv) != 2:
        print("Usage: create_database.py <database name>")
        sys.exit(1)

    db_name = sys.argv[1]
    db_file = f'{db_name}.sqlite3'

    engine = create_engine(f'sqlite:///{db_file}')
    Base.metadata.create_all(engine)

    print("Database created successfully")

if __name__ == '__main__':
    main()
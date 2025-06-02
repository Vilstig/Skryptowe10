import sys
import sqlite3

def main():
    if len(sys.argv) != 2:
        print("Usage: python create_database_sql.py <database_name>")
        sys.exit(1)

    db_name = sys.argv[1]
    db_file = f"{db_name}.sqlite3"
    schema_file = "schema.sql"

    with open(schema_file, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()

    print(f"Baza danych {db_file} została utworzona na podstawie {schema_file}")

if __name__ == "__main__":
    main()

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DATABASE = 'rentals.sqlite3'

def get_stations():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    stations = conn.execute("SELECT station_id, station_name FROM stations ORDER BY station_name").fetchall()
    conn.close()
    return stations

@app.route('/', methods=['GET', 'POST'])
def index():
    stations = get_stations()
    result = None
    selected_station_id = request.form.get('station_id')
    button = request.form.get('action')
    selected_station_name = None

    if request.method == 'POST' and selected_station_id and button:
        selected_station_name = next(
            (s['station_name'] for s in stations if str(s['station_id']) == selected_station_id), None
        )

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()

        if button == 'avg_start':
            cur.execute("SELECT AVG(duration) FROM rentals WHERE rental_station = ?", (selected_station_id,))
            result = f"Średni czas rozpoczęcia: {round(cur.fetchone()[0] or 0, 2)} min"

        elif button == 'avg_end':
            cur.execute("SELECT AVG(duration) FROM rentals WHERE return_station = ?", (selected_station_id,))
            result = f"Średni czas zakończenia: {round(cur.fetchone()[0] or 0, 2)} min"

        elif button == 'unique_bikes':
            cur.execute("SELECT COUNT(DISTINCT bike_number) FROM rentals WHERE return_station = ?", (selected_station_id,))
            result = f"Liczba różnych rowerów: {cur.fetchone()[0]}"

        elif button == 'round_trips':
            cur.execute("""
                SELECT COUNT(*) FROM rentals
                WHERE rental_station = ? AND return_station = ?
            """, (selected_station_id, selected_station_id))
            result = f"Liczba wypożyczeń zaczynających i kończących się na tej samej stacji: {cur.fetchone()[0]}"

        conn.close()

    return render_template('index.html', stations=stations, result=result, station_name=selected_station_name)



if __name__ == '__main__':
    app.run(debug=True) # runs on localhost:5000
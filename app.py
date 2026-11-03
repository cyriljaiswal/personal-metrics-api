from flask import Flask, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return {"status": "Personal Metrics API is running"}

@app.route('/api/logs', methods=['POST'])
def add_log():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO logs (log_date, category, duration_minutes, notes) VALUES (?, ?, ?, ?)',
                 (data['log_date'], data['category'], data.get('duration_minutes', 0), data.get('notes', '')))
    conn.commit()
    conn.close()
    return {"status": "Log added successfully"}, 201

if __name__ == '__main__':
    app.run(debug=True)
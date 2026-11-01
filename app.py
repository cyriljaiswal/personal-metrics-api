from flask import Flask
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return {"status": "Personal Metrics API is running"}

if __name__ == '__main__':
    app.run(debug=True)
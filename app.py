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
    
    # Validation Check
    if not data or 'log_date' not in data or 'category' not in data:
        return {"error": "Missing required fields. 'log_date' and 'category' are mandatory."}, 400

    conn = get_db_connection()
    conn.execute('INSERT INTO logs (log_date, category, duration_minutes, notes) VALUES (?, ?, ?, ?)',
                 (data['log_date'], data['category'], data.get('duration_minutes', 0), data.get('notes', '')))
    conn.commit()
    conn.close()
    return {"status": "Log added successfully"}, 201

@app.route('/api/logs', methods=['GET'])
def get_logs():
    category = request.args.get('category')
    limit = request.args.get('limit', 50)
    conn = get_db_connection()
    if category:
        logs = conn.execute('SELECT * FROM logs WHERE category = ? LIMIT ?', (category, limit)).fetchall()
    else:
        logs = conn.execute('SELECT * FROM logs LIMIT ?', (limit,)).fetchall()
    conn.close()
    return {"logs": [dict(log) for log in logs]}, 200

@app.route('/api/logs/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    conn = get_db_connection()
    cursor = conn.execute('DELETE FROM logs WHERE id = ?', (log_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    
    if rows_affected == 0:
        return {"error": "Log not found"}, 404
        
    return {"status": f"Log {log_id} deleted successfully"}, 200

@app.route('/api/summary', methods=['GET'])
def get_summary():
    conn = get_db_connection()
    summary = conn.execute('''
        SELECT category, SUM(duration_minutes) as total_minutes, COUNT(id) as total_logs 
        FROM logs 
        GROUP BY category
    ''').fetchall()
    conn.close()
    return {"summary": [dict(row) for row in summary]}, 200

@app.route('/api/logs/<int:log_id>', methods=['PUT'])
def update_log(log_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.execute('''
        UPDATE logs 
        SET log_date = ?, category = ?, duration_minutes = ?, notes = ?
        WHERE id = ?
    ''', (data['log_date'], data['category'], data.get('duration_minutes', 0), data.get('notes', ''), log_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    
    if rows_affected == 0:
        return {"error": "Log not found"}, 404
        
    return {"status": f"Log {log_id} updated successfully"}, 200

if __name__ == '__main__':
    app.run(debug=True)
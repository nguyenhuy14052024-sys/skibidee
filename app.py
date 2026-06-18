from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('daily_logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS switch_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/log', methods=['POST'])
def save_log():
    data = request.get_json()
    state = data.get('state')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('daily_logs.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO switch_history (state, timestamp) VALUES (?, ?)", (state, current_time))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "saved": state, "time": current_time})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def init_db():
    # Sửa lỗi: Tạo kết nối SQLite ngay trong hàm
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
    
    return jsonify({"status": "success", "time": current_time})

if __name__ == '__main__':
    # Chạy hàm khởi tạo database trước khi mở server
    init_db()
    
    # Sửa lỗi Port trên Render: Lấy cổng do Render cấp, nếu không có thì dùng 5000
    port = int(os.environ.get("PORT", 5000))
    
    # Bắt buộc phải có host='0.0.0.0' để Render kết nối được
    app.run(host='0.0.0.0', port=port)
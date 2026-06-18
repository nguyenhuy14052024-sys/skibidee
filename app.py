import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Tên file Database
DB_NAME = 'daily_logs.db'

def init_db():
    # Sửa lỗi: Tạo kết nối SQLite ngay trong hàm
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tạo bảng với ID tự tăng để quản lý chính xác
    cursor.execute(f'''
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
    # Khi load trang, bạn có thể gửi dữ liệu lịch sử về (bước nâng cấp sau)
    return render_template('index.html')

@app.route('/api/log', methods=['POST'])
def save_log():
    data = request.get_json()
    state = data.get('state')
    current_time = datetime.now().strftime("%H:%M:%S") # Chỉ lấy giờ phút giây cho đẹp
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO switch_history (state, timestamp) VALUES (?, ?)", (state, current_time))
    conn.commit()
    conn.close()
    
    # Trả về status và thời gian đã lưu để frontend cập nhật
    return jsonify({"status": "success", "time": current_time})

from flask import send_from_directory

@app.route('/favicon.svg')
def favicon():
    # Hàm này giúp trả về file logo khi trình duyệt yêu cầu
    return send_from_directory(os.path.join(app.root_path),
                               'favicon.svg', mimetype='image/svg+xml')
if __name__ == '__main__':
    # Khởi tạo database trước khi mở server
    init_db()
    
    # Cấu hình Port trên Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
# file: server.py
# Flask server for Smart Farm application

from config import DB_PATH, IMAGE_PATH, REMOTE_PI_IP
from flask import Flask, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime, timedelta
from image_processing import analyze_growth_stage

app = Flask(__name__)

# -------------------------------
# 최근 센서 데이터 조회
# -------------------------------
def fetch_sensor_data():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, timestamp, temperature, humidity, moisture, water_level, growth_level, confidence
                FROM sensor_data
                ORDER BY timestamp DESC
                LIMIT 10
            ''')
            rows = cursor.fetchall()

            if not rows:
                return {'message': 'No sensor data available'}

            sensor_list = [
                {
                    'id': r[0],
                    'timestamp': r[1],
                    'temperature': r[2],
                    'humidity': r[3],
                    'moisture': r[4],
                    'water_level': r[5],
                    'growth_level': r[6],
                    'confidence': r[7]
                }
                for r in rows
            ]
            return {'sensor_data': sensor_list}

    except sqlite3.Error as e:
        print(f'[Server][DB Error] {e}')
        return {'error': f'Database error: {e}'}


# -------------------------------
# 최신 이미지로 성장 단계 분석
# -------------------------------
def analyze_growth_stage_latest():
    try:
        files = sorted([f for f in os.listdir(IMAGE_PATH) if f.endswith('.jpg')])
        if not files:
            return {'error': 'No images found'}

        latest_image = files[-1]
        image_path = os.path.join(IMAGE_PATH, latest_image)

        result = analyze_growth_stage(image_path)
        if not result:
            return {'error': 'Growth analysis failed'}

        return {
            'growth_stage': result['growth_level'],
            'confidence': result['confidence'],
            'label': result['label']
        }

    except Exception as e:
        print(f'[Server][Analysis Error] {e}')
        return {'error': f'Growth analysis error: {e}'}


# -------------------------------
# 최근 7일 이미지 목록 반환
# -------------------------------
@app.route('/latest_images')
def get_latest_images():
    try:
        files = sorted(os.listdir(IMAGE_PATH))
        if not files:
            return jsonify({'error': 'No images found'}), 404

        one_week_ago = datetime.now() - timedelta(days=7)
        recent_files = []
        for f in files:
            path = os.path.join(IMAGE_PATH, f)
            if os.path.isfile(path):
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                if mtime >= one_week_ago:
                    recent_files.append(f)

        recent_files = sorted(
            recent_files,
            key=lambda x: os.path.getmtime(os.path.join(IMAGE_PATH, x)),
            reverse=True
        )

        return jsonify({'images': recent_files})
    except Exception as e:
        print(f'[Server][Image Error] {e}')
        return jsonify({'error': f'Image listing error: {e}'}), 500


# -------------------------------
# 개별 이미지 제공
# -------------------------------
@app.route('/image/<filename>')
def get_image(filename):
    safe_name = secure_filename(filename)
    return send_from_directory(IMAGE_PATH, safe_name)


# -------------------------------
# Flask 라우트
# -------------------------------
@app.route('/sensor_data')
def get_sensor_data():
    return jsonify(fetch_sensor_data())


@app.route('/growth_stage')
def get_growth_stage():
    return jsonify(analyze_growth_stage_latest())


@app.route('/config')
def get_config():
    return jsonify({'pi_ip': REMOTE_PI_IP})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
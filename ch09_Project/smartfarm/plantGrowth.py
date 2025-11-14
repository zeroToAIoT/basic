# file: plantGrowth.py

import os
import sqlite3
import time
from datetime import datetime
from threading import Lock # main.py와 _system_status를 공유 Lock 임포트

from config import DB_PATH, IMAGE_PATH
from image_processing import analyze_growth_stage

def save_sensor_data(temp, hum, moisture, water_level, growth_level, confidence):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sensor_data 
                (temperature, humidity, moisture, water_level, growth_level, confidence, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (temp, hum, moisture, water_level, growth_level, confidence, datetime.now()))
            conn.commit()
            print(f'[PlantGrowth][DB] Saved: T={temp}, H={hum}, M={moisture}, '
                  f'W={water_level}, G={growth_level}, C={confidence:.2f}')
    except sqlite3.Error as err:
        print(f'[PlantGrowth][DB Error] {err}')


def analyze_growth_stage_latest(system_status_lock, system_status):
    """
    Analyze growth stage from the latest image
    main.py의 _system_status를 참조하여 growth_level과 confidence를 업데이트
    """
    try:
        files = sorted([f for f in os.listdir(IMAGE_PATH) if f.endswith(".jpg")])
        if not files:
            print("[PlantGrowth] No images found to analyze.")
            return None, None 

        latest_image = files[-1]
        image_path = os.path.join(IMAGE_PATH, latest_image)

        result = analyze_growth_stage(image_path) # AI 추론 실행
        if result:
            growth_level = result.get("growth_level")
            confidence = result.get("confidence")
            
            with system_status_lock:
                system_status['growth_level'] = growth_level
                system_status['growth_confidence'] = confidence

            return growth_level, confidence
        return None, None

    except Exception as err:
        print(f'[PlantGrowth][Analysis Error] {err}')
        return None, None


def growth_analysis_loop(stop_event, interval, system_status_lock, system_status):
    """
    Loop for analyzing growth stage and saving to DB
    main.py로부터 _system_status를 받아서 DB에 저장
    """
    print("[PlantGrowth] Analysis & DB Save loop started...")
    while not stop_event.is_set():
        # 1. AI 추론 실행 및 _system_status 업데이트
        growth_level, confidence = analyze_growth_stage_latest(system_status_lock, system_status)

        if growth_level is not None and confidence is not None:
            # 2. main.py가 업데이트한 _system_status에서 값을 가져옴
            try:
                with system_status_lock: 
                    temp = system_status.get('temp')
                    hum = system_status.get('hum')
                    moisture = system_status.get('moisture')
                    water_level = system_status.get('water_level')

                # 3. DB에 저장
                save_sensor_data(temp, hum, moisture, water_level, growth_level, confidence)

            except Exception as e:
                print(f'[PlantGrowth][Sensor Error] {e}')
        
        # 4. interval (12시간) 동안 대기
        print(f"[PlantGrowth] Next analysis in {interval} seconds...")
        for _ in range(interval):
            if stop_event.is_set():
                break
            time.sleep(1)
    print("[PlantGrowth] Analysis & DB Save loop stopped.")

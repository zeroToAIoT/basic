# file: plantGrowth.py
# Plant Growth Monitoring Module (Refactored)

import os
import sqlite3
import time
from datetime import datetime
from threading import Event, Thread

from config import DB_PATH, IMAGE_PATH, CAMERA_INTERVAL
from camera import capture_image_loop
from image_processing import analyze_growth_stage


def save_sensor_data(temp, hum, moisture, water_level, growth_level, confidence):
    """Save sensor data to database"""
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
    except sqlite3.Error as e:
        print(f'[PlantGrowth][DB Error] {e}')


def analyze_growth_stage_latest():
    """Analyze growth stage from the latest image"""
    try:
        files = sorted([f for f in os.listdir(IMAGE_PATH) if f.endswith(".jpg")])
        if not files:
            return None, None

        latest_image = files[-1]
        image_path = os.path.join(IMAGE_PATH, latest_image)

        result = analyze_growth_stage(image_path)
        if result:
            return result.get("growth_level"), result.get("confidence")
        return None, None

    except Exception as e:
        print(f'[PlantGrowth][Analysis Error] {e}')
        return None, None


def growth_analysis_loop(stop_event, interval):
    """Loop for analyzing growth stage and saving to DB"""
    while not stop_event.is_set():
        growth_level, confidence = analyze_growth_stage_latest()

        if growth_level is not None and confidence is not None:
            try:
                from temp_hum import read_temp_hum
                from moisture import read_moisture
                from waterSensor import read_water_level

                temp, hum = read_temp_hum()
                moisture = read_moisture()
                water_level = read_water_level()

                save_sensor_data(temp, hum, moisture, water_level, growth_level, confidence)

            except Exception as e:
                print(f'[PlantGrowth][Sensor Error] {e}')

        # interval 동안 대기
        for _ in range(interval):
            if stop_event.is_set():
                break
            time.sleep(1)


def update_plant_growth():
    """Main entry point: start camera capture and growth analysis in parallel"""
    stop_event = Event()

    camera_thread = Thread(target=capture_image_loop,
                           args=(stop_event, IMAGE_PATH, CAMERA_INTERVAL),
                           daemon=True)
    analysis_thread = Thread(target=growth_analysis_loop,
                             args=(stop_event, CAMERA_INTERVAL),
                             daemon=True)

    camera_thread.start()
    analysis_thread.start()

    print("[PlantGrowth][System] Monitoring started.")

    try:
        camera_thread.join()
        analysis_thread.join()
    except KeyboardInterrupt:
        print("[PlantGrowth][System] Stopping monitoring...")
        stop_event.set()
        camera_thread.join()
        analysis_thread.join()
        print("[PlantGrowth][System] Monitoring stopped.")
    except Exception as e:
        print(f"[PlantGrowth][System Error] {e}")
        stop_event.set()
        camera_thread.join()
        analysis_thread.join()
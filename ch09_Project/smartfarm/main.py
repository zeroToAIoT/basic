# file: main.py
# SmartFarm Main System (Final Refactored Version)

import threading
from signal import pause
from time import sleep

from lcd import display_lcd
from supplyWaterMoisture import control_water_pump
from supplyWaterTank import control_water_tank
from music import play_music, start_music
from plantGrowth import update_plant_growth, analyze_growth_stage_latest
from bluedot import start_bluedot, set_bluedot
from button import set_button
from rgbled import update_rgbled

# read sensor values
from temp_hum import read_temp_hum
from moisture import read_moisture
from waterSensor import read_water_level
from buzzer import check_and_alert
from light import read_light_sensor

# config import
from config import IMAGE_PATH, CAMERA_INTERVAL, DB_PATH

smartFarm_active = False
stop_event = threading.Event()


def sensor_monitor():
    """주기적으로 센서값 읽고 RGB LED 및 알람 제어"""
    while get_system_status():
        try:
            light_value = read_light_sensor()
            temp, hum = read_temp_hum()
            moisture_value = read_moisture()
            water_level_value = read_water_level()
            growth_level_value, confidence = analyze_growth_stage_latest()

            update_rgbled(light_value, growth_level_value, confidence)
            check_and_alert(temp, hum, moisture_value, water_level_value)

        except Exception as e:
            print(f"[Sensor Monitor Error] {e}")

        sleep(10)


def activate():
    """스마트팜 시스템 활성화"""
    global smartFarm_active
    if smartFarm_active:
        print('SmartFarm System already activated')
        return

    smartFarm_active = True
    stop_event.clear()
    print('SmartFarm System Activated')

    # 병렬 실행 모듈들
    threading.Thread(target=display_lcd, daemon=True).start()
    threading.Thread(target=control_water_pump, daemon=True).start()
    threading.Thread(target=control_water_tank, daemon=True).start()
    threading.Thread(target=start_music, daemon=True).start()
    threading.Thread(target=play_music, daemon=True).start()
    threading.Thread(target=update_plant_growth, daemon=True).start()  # 인자 제거
    threading.Thread(target=sensor_monitor, daemon=True).start()


def deactivate():
    """스마트팜 시스템 비활성화"""
    global smartFarm_active
    if not smartFarm_active:
        print('SmartFarm System already deactivated')
        return

    smartFarm_active = False
    stop_event.set()
    print('SmartFarm System Deactivated')


def get_system_status():
    return smartFarm_active and not stop_event.is_set()


def main():
    set_button(activate, deactivate, get_system_status)
    set_bluedot(activate, deactivate)

    start_bluedot()

    print('Starting SmartFarm System...')
    activate()

    try:
        pause()
    except KeyboardInterrupt:
        print('SmartFarm System stopped. Ctrl+C.')
    except Exception as err:
        print(f'SmartFarm MainSystem Error: {err}')
    finally:
        deactivate()


if __name__ == '__main__':
    main()
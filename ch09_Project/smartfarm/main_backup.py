# file: main.py
# SmartFarm Main System

import threading
from signal import pause
from time import sleep

from lcd import display_lcd
from supplyWaterMoisture import control_water_pump
from supplyWaterTank import control_water_tank
from music import play_music, start_music
from plantGrowth import update_plant_growth
from bluedot import start_bluedot, set_bluedot
from button import set_button
from rgbled import update_rgbled

# read sensor values
from temp_hum import read_temp_hum
from moisture import read_moisture
from waterSensor import read_water_level
from buzzer import check_and_alert
from light import read_light_sensor
from plantGrowth import analyze_growth_stage_latest

# config import
from config import IMAGE_PATH, CAMERA_INTERVAL, DB_PATH

smartFarm_active = False
stop_event = threading.Event()


def sensor_monitor():
    while get_system_status():
        light_value = read_light_sensor()
        temp, hum = read_temp_hum()
        moisture_value = read_moisture()
        water_level_value = read_water_level()
        growth_level_value, confidence = analyze_growth_stage_latest()
        update_rgbled(light_value, growth_level_value, confidence)
        check_and_alert(light_value, temp, hum, moisture_value, water_level_value)

        sleep(10)


def activate():
    global smartFarm_active
    if smartFarm_active:
        print('SmartFarm System already activated')
        return

    smartFarm_active = True
    stop_event.clear()
    print('SmartFarm System Activated')

    threading.Thread(target=display_lcd, daemon=True).start()
    threading.Thread(target=control_water_pump, daemon=True).start()
    threading.Thread(target=control_water_tank, daemon=True).start()
    threading.Thread(target=start_music, daemon=True).start()
    threading.Thread(target=play_music, daemon=True).start()
    threading.Thread(
        target=update_plant_growth,
        args=(stop_event, IMAGE_PATH, CAMERA_INTERVAL, DB_PATH),
        daemon=True
    ).start()
    threading.Thread(target=sensor_monitor, daemon=True).start()


def deactivate():
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
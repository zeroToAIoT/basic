# file: supplyWaterMoisture.py
# Supply Water Module using Moisture Sensor

from time import sleep
from gpiozero import Motor

from config import PIN, get_threshold, WATER_PUMP_INTERVAL
from moisture import read_moisture

water_pump = Motor(PIN['WATER_PUMP'])

def control_water_pump():
    """Control water pump based on moisture sensor reading"""
    try:
        moisture_value = read_moisture()
        low_threshold = get_threshold('moisture_low')
        high_threshold = get_threshold('moisture_high')

        if moisture_value is not None:
            if moisture_value <= low_threshold:
                print(f'[WaterPump] Moisture Low ({moisture_value:.2f}%) → Pump ON')
                water_pump.forward()
            elif moisture_value >= high_threshold:
                print(f'[WaterPump] Moisture Sufficient ({moisture_value:.2f}%) → Pump OFF')
                water_pump.stop()
            else:
                print(f'[WaterPump] Moisture Normal ({moisture_value:.2f}%) → Pump OFF')
                water_pump.stop()
        else:
            print('[WaterPump] Failed.. Moisture data unavailable. Pump OFF')
            water_pump.stop()

    except KeyboardInterrupt:
        print('[WaterPump] Stopped by Ctrl+C')
        water_pump.stop()
    except Exception as err:
        print(f'[WaterPump Error] {err}')
        water_pump.stop()


def water_pump_loop(stop_event):
    """Loop to control water pump periodically until stop_event is set"""
    try:
        while not stop_event.is_set():
            control_water_pump()
            for _ in range(WATER_PUMP_INTERVAL):
                if stop_event.is_set():
                    break
                sleep(1)
    except Exception as err:
        print(f'[WaterPump Error] in loop: {err}')
        water_pump.stop()


# Manual control functions for BlueDot
def pump_on():
    """Manually turn on the water pump"""
    try:
        water_pump.forward()
        print('[WaterPump] Manually turned ON')
    except Exception as e:
        print(f'[WaterPump Error] turning on: {e}')


def pump_off():
    """Manually turn off the water pump"""
    try:
        water_pump.stop()
        print('[WaterPump] Manually turned OFF')
    except Exception as e:
        print(f'[WaterPump Error] turning off: {err}')
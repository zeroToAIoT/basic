# file: supplyWaterTank.py
# Supply Water to Tank using Water Level Sensor and Servo Motor

from time import sleep
from gpiozero import Servo

from config import PIN, get_threshold, WATER_TANK_INTERVAL
from waterSensor import read_water_level

servo = Servo(PIN['SERVO'])

def control_water_tank(water_level_value):
    try:
        low_threshold = get_threshold('water_low')
        high_threshold = get_threshold('water_high')

        if water_level_value is not None:
            if water_level_value <= low_threshold:
                print(f'[WaterTank] Level Low ({water_level_value:.2f}%) → Opening Valve')
                servo.max()
            elif water_level_value >= high_threshold:
                print(f'[WaterTank] Level Sufficient ({water_level_value:.2f}%) → Closing Valve')
                servo.min()
            else:
                print(f'[WaterTank] Level Normal ({water_level_value:.2f}%) → Valve Closed')
                servo.min()
        else:
            print('[WaterTank] Failed.. Water level data unavailable. Valve Closed')
            servo.min()

    except KeyboardInterrupt:
        print('[WaterTank] Control stopped manually (Ctrl+C)')
        servo.min()
    except Exception as err:
        print(f'[WaterTank Error] {err}')
        servo.min()


def water_tank_loop(stop_event):
    """Loop to control water tank periodically until stop_event is set"""
    try:
        while not stop_event.is_set():
            control_water_tank(read_water_level())
            for _ in range(WATER_TANK_INTERVAL):
                if stop_event.is_set():
                    break
                sleep(1)
    except Exception as err:
        print(f'[WaterTank Error] in loop: {err}')
        servo.min()


# Manual control functions for BlueDot
def tank_open():
    """Manually open the water tank valve"""
    try:
        servo.max()
        print('[WaterTank] Valve manually opened')
    except Exception as err:
        print(f'[WaterTank Error] opening valve: {err}')


def tank_close():
    """Manually close the water tank valve"""
    try:
        servo.min()
        print('[WaterTank] Valve manually closed')
    except Exception as err:
        print(f'[WaterTank Error] closing valve: {err}')
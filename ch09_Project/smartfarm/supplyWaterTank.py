# file: supplyWaterTank.py

from time import sleep
from gpiozero import Servo
from config import PIN, get_threshold

servo = Servo(PIN['SERVO'])
_is_valve_open = False
_manual_mode = False

def control_water_tank_auto(water_level_value, manual_mode):
    global _is_valve_open, _manual_mode
    _manual_mode = manual_mode

    if _manual_mode:
        return 

    try:
        low_threshold = get_threshold('water_low')
        high_threshold = get_threshold('water_high')

        if water_level_value is not None:
            if water_level_value <= low_threshold:
                if not _is_valve_open:
                    print(f'[WaterTank] Level Low ({water_level_value:.2f}%) → Opening Valve')
                    servo.max()
                    _is_valve_open = True
            elif water_level_value >= high_threshold:
                if _is_valve_open:
                    print(f'[WaterTank] Level Sufficient ({water_level_value:.2f}%) → Closing Valve')
                    servo.min()
                    _is_valve_open = False
            else:
                if _is_valve_open: # 정상 범위일 때도 밸브를 닫음
                    print(f'[WaterTank] Level Normal ({water_level_value:.2f}%) → Valve Closed')
                    servo.min()
                    _is_valve_open = False
        else:
            if _is_valve_open:
                print('[WaterTank] Failed sensor data. Valve Closed (Auto) for safety.')
                servo.min()
                _is_valve_open = False

    except Exception as err:
        print(f'[WaterTank Error] {err}')
        servo.min()
        _is_valve_open = False


def tank_open():
    global _is_valve_open, _manual_mode
    try:
        servo.max()
        _is_valve_open = True
        _manual_mode = True
        print('[WaterTank] Valve manually opened')
    except Exception as err:
        print(f'[WaterTank Error] opening valve: {err}')

def tank_close():
    global _is_valve_open, _manual_mode
    try:
        servo.min()
        _is_valve_open = False
        _manual_mode = True
        print('[WaterTank] Valve manually closed')
    except Exception as err:
        print(f'[WaterTank Error] closing valve: {err}')

def get_tank_manual_mode():
    return _manual_mode

def water_tank_cleanup():
    servo.min()
    servo.close()
    print("[WaterTank] Resource released.")
# file: supplyWaterMoisture.py
from time import sleep
from gpiozero import Motor
from config import PIN, get_threshold

water_pump = Motor(PIN['WATER_PUMP'])
_is_pump_on = False
_manual_mode = False 

def control_water_pump_auto(moisture_value, manual_mode):
    """ 자동 펌프 제어 (main.py의 중앙 루프에서 호출됨) """
    global _is_pump_on, _manual_mode
    _manual_mode = manual_mode

    if _manual_mode:
        return # 수동 모드일 땐 자동 제어 안 함

    try:
        low_threshold = get_threshold('moisture_low')
        high_threshold = get_threshold('moisture_high')

        if moisture_value is not None:
            if moisture_value <= low_threshold:
                if not _is_pump_on:
                    print(f'[WaterPump] ON (Auto): Moisture Low ({moisture_value:.2f}%)')
                    water_pump.forward()
                    _is_pump_on = True
            elif moisture_value >= high_threshold:
                if _is_pump_on:
                    print(f'[WaterPump] OFF (Auto): Moisture Sufficient ({moisture_value:.2f}%)')
                    water_pump.stop()
                    _is_pump_on = False
        else:
            if _is_pump_on:
                print('[WaterPump] Failed sensor data. Pump OFF (Auto) for safety.')
                water_pump.stop()
                _is_pump_on = False
    except Exception as err:
        print(f'[WaterPump Error] {err}')
        water_pump.stop()
        _is_pump_on = False

# (manual functions)
def pump_on():
    global _is_pump_on, _manual_mode
    try:
        water_pump.forward()
        _is_pump_on = True
        _manual_mode = True
        print('[WaterPump] Manually turned ON')
    except Exception as e:
        print(f'[WaterPump Error] turning on: {e}')

def pump_off():
    global _is_pump_on, _manual_mode
    try:
        water_pump.stop()
        _is_pump_on = False
        _manual_mode = True
        print('[WaterPump] Manually turned OFF')
    except Exception as e:
        print(f'[WaterPump Error] turning off: {e}')

def get_pump_manual_mode():
    return _manual_mode

def water_pump_cleanup():
    water_pump.stop()
    water_pump.close()
    print("[WaterPump] Resource released.")
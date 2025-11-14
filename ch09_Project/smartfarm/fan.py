# file: fan.py

from time import sleep
from gpiozero import Motor
from config import PIN, get_threshold

fan = Motor(PIN['FAN'])
_is_fan_on = False
_manual_mode = False # 수동 모드 플래그

def control_fan_auto(temp, hum, manual_mode):
    """ 자동 팬 제어 (main.py의 중앙 루프에서 호출됨) """
    global _is_fan_on, _manual_mode
    _manual_mode = manual_mode # 현재 모드를 메인에서 받아옴
    
    if _manual_mode:
        # 수동 모드일 때는 자동 제어 로직을 건너뜀
        return 
        
    try:
        if temp is not None and hum is not None:
            if temp >= get_threshold('temp_high') or hum <= get_threshold('hum_low'):
                if not _is_fan_on:
                    print(f'[Fan] ON (Auto): Temp={temp:.1f}, Hum={hum:.1f}')
                    fan.forward()
                    _is_fan_on = True
            else:
                if _is_fan_on:
                    print(f'[Fan] OFF (Auto): Temp={temp:.1f}, Hum={hum:.1f}')
                    fan.stop()
                    _is_fan_on = False
        else:
            if _is_fan_on:
                print('[Fan] Failed sensor data. Fan OFF (Auto) for safety.')
                fan.stop()
                _is_fan_on = False
    except Exception as e:
        fan.stop()
        _is_fan_on = False
        print(f'[Fan Error] {e}')

def fan_on():
    """ 수동 제어: 팬 켜기 (BlueDot용) """
    global _is_fan_on, _manual_mode
    try:
        fan.forward()
        _is_fan_on = True
        _manual_mode = True # 수동 모드로 전환
        print('[Fan] Manually turned ON')
    except Exception as e:
        print(f'[Fan Error] turning on: {e}')

def fan_off():
    """ 수동 제어: 팬 끄기 (BlueDot용) """
    global _is_fan_on, _manual_mode
    try:
        fan.stop()
        _is_fan_on = False
        _manual_mode = True # 수동 모드로 전환 (자동 재시작 방지)
        print('[Fan] Manually turned OFF')
    except Exception as e:
        print(f'[Fan Error] turning off: {e}')

def get_fan_manual_mode():
    """ main.py가 현재 수동 모드인지 확인하기 위한 함수 """
    return _manual_mode

def fan_cleanup():
    fan.stop()
    fan.close()
    print("[Fan] Resource released.")
# file: light_module.py
# Light Sensor Module (Monitoring Loop Added)

from gpiozero import MCP3008
from config import MCP3008_CHANNEL
from time import sleep
from system_status import is_system_active
import threading

# get the MCP3008 channel for the light sensor
light_sensor = MCP3008(channel=MCP3008_CHANNEL['LIGHT_SENSOR'])

# 현재 조도 값을 저장하는 변수
_current_light_value = None
_status_lock = threading.Lock()  # 스레드 안전성을 위한 Lock

def read_light_value():
    """조도 센서의 현재 값을 한 번 읽어서 반환"""
    try:
        global _current_light_value
        with _status_lock:
            _current_light_value = light_sensor.value
        # print(f'Light Value: {_current_light_value:.8f}') # 너무 자주 출력될 수 있으므로 주석 처리 또는 로그로 변경
        return _current_light_value
    except Exception as err:
        print(f'LightSensor Error : {err}')
        with _status_lock:
            _current_light_value = None
        return None

def get_current_light_value():
    """외부에서 현재 조도 값을 가져오는 함수 (스레드 안전)"""
    with _status_lock:
        return _current_light_value

def monitor_light_sensor():
    """조도 센서를 무한 루프하며 지속적으로 모니터링하는 스레드 대상 함수"""
    print("Light sensor monitoring started...")
    error_count = 0
    max_errors = 5
    
    while is_system_active():
        try:
            read_light_value() # 주기적으로 조도 값 읽기
            error_count = 0  # 성공 시 에러 카운터 리셋
            sleep(3) # 3초마다 체크
        except Exception as e:
            error_count += 1
            print(f"Light Monitoring Error ({error_count}/{max_errors}): {e}")
            
            if error_count >= max_errors:
                print("Light sensor disabled due to repeated errors.")
                break  # 심각한 오류 시 해당 모듈만 비활성화
            
            sleep(5) # 오류 발생 시 잠시 대기 후 재시도
    print("Light sensor monitoring stopped.")

def cleanup():
    """리소스 정리 함수"""
    global light_sensor
    try:
        if light_sensor:
            light_sensor.close()
        print("Light module cleaned up.")
    except Exception as e:
        print(f"Light module cleanup error: {e}")
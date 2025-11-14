# file: fire_module.py
# Fire Detection Module (Monitoring Loop Added)

from gpiozero import MCP3008
from config import THRESHOLDS, MCP3008_CHANNEL
from time import sleep
from system_status import is_system_active
import threading

fire_sensor = MCP3008(MCP3008_CHANNEL['FIRE_SENSOR'])

# 현재 화재 감지 상태를 저장하는 변수 (main.py에서 참조할 수 있도록)
_fire_alert_active = False
_status_lock = threading.Lock()  # 스레드 안전성을 위한 Lock

def read_fire_value():
    """화재 센서의 현재 값을 한 번 읽어서 반환"""
    try:
        fire_level = fire_sensor.value
        # print(f'Fire Sensor Value: {fire_level:.2f}') # 너무 자주 출력될 수 있으므로 주석 처리 또는 로그로 변경
        return fire_level
    except Exception as err:
        print(f'Fire Sensor Error: {err}')
        return None
  
def fire_detect():
    """화재 감지 로직을 수행하고, 상태만 업데이트 (제어는 main.py에서 수행)"""
    global _fire_alert_active
    fire_level = read_fire_value()
    
    with _status_lock:
        if fire_level is not None and fire_level > THRESHOLDS['FIRE_HIGH']:
            if not _fire_alert_active: # 새로 감지된 경우에만 출력
                print('Fire detected! Alerting system...')
            _fire_alert_active = True
            return True
        else:
            if _fire_alert_active: # 화재 감지 상태였다가 해제된 경우에만 출력
                print('No fire detected. Clearing alert.')
            _fire_alert_active = False
            return False

def get_current_fire_status():
    """외부에서 현재 화재 감지 상태를 가져오는 함수 (스레드 안전)"""
    with _status_lock:
        return _fire_alert_active

def monitor_fire_sensor():
    """화재 센서를 무한 루프하며 지속적으로 모니터링하는 스레드 대상 함수"""
    print("Fire sensor monitoring started...")
    error_count = 0
    max_errors = 5
    
    while is_system_active():
        try:
            fire_detect() # 주기적으로 화재 감지 로직 실행
            error_count = 0  # 성공 시 에러 카운터 리셋
            sleep(2) # 2초마다 체크
        except Exception as e:
            error_count += 1
            print(f"Fire Monitoring Error ({error_count}/{max_errors}): {e}")
            
            if error_count >= max_errors:
                print("Fire sensor disabled due to repeated errors.")
                break  # 심각한 오류 시 해당 모듈만 비활성화
            
            sleep(5) # 오류 발생 시 잠시 대기 후 재시도
    print("Fire sensor monitoring stopped.")

def cleanup():
    """리소스 정리 함수"""
    global fire_sensor
    try:
        if fire_sensor:
            fire_sensor.close()
        print("Fire module cleaned up.")
    except Exception as e:
        print(f"Fire module cleanup error: {e}")
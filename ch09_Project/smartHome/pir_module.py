# file: pir_module.py
# PIR Sensor Module (Monitoring Loop Added)

from gpiozero import MotionSensor
from config import PIN
from camera_module import capture_image
from time import sleep
from system_status import is_system_active
import threading

pir_door = MotionSensor(PIN['PIR_DOOR'])
pir_window = MotionSensor(PIN['PIR_WINDOW'])

# 현재 감지 상태를 저장하는 변수 (main.py에서 이 값을 참조할 수 있도록)
_motion_detected_at = None
_status_lock = threading.Lock()  # 스레드 안전성을 위한 Lock

def read_pir_status():
    """PIR 센서의 현재 감지 상태를 한 번 읽어서 반환"""
    global _motion_detected_at
    with _status_lock:
        if pir_door.motion_detected:
            _motion_detected_at = 'door'
            print('Motion detected at door')
            print('Capturing image...')
            capture_image('door')
            return 'door'
        elif pir_window.motion_detected:
            _motion_detected_at = 'window'
            print('Motion detected at window')
            print('Capturing image...')
            capture_image('window')
            return 'window'
        else:
            if _motion_detected_at is not None: # 움직임이 있다가 사라지면 None으로 리셋
                print('Motion cleared.')
            _motion_detected_at = None
            return None

def get_current_motion_status():
    """외부에서 현재 감지된 움직임 위치를 가져오는 함수 (스레드 안전)"""
    with _status_lock:
        return _motion_detected_at

def monitor_pir_sensors():
    """PIR 센서를 무한 루프하며 지속적으로 모니터링하는 스레드 대상 함수"""
    print("PIR sensor monitoring started...")
    error_count = 0
    max_errors = 5
    
    while is_system_active():
        try:
            read_pir_status() # 주기적으로 PIR 상태를 읽고 업데이트
            error_count = 0  # 성공 시 에러 카운터 리셋
            sleep(1) # 1초마다 체크
        except Exception as e:
            error_count += 1
            print(f"PIR Monitoring Error ({error_count}/{max_errors}): {e}")
            
            if error_count >= max_errors:
                print("PIR sensor disabled due to repeated errors.")
                break  # 심각한 오류 시 해당 모듈만 비활성화
            
            sleep(5) # 오류 발생 시 잠시 대기 후 재시도
    print("PIR sensor monitoring stopped.")

def cleanup():
    """리소스 정리 함수"""
    global pir_door, pir_window
    try:
        if pir_door:
            pir_door.close()
        if pir_window:
            pir_window.close()
        print("PIR module cleaned up.")
    except Exception as e:
        print(f"PIR module cleanup error: {e}")
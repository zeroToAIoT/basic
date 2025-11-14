# file: temp_hum_module.py
# Temperature and Humidity Sensor Module using DHT11 (Monitoring Loop Added)

from adafruit_dht import DHT11
from config import PIN
import board # board.D17 사용을 위해 필요
from time import sleep
from system_status import is_system_active
import threading

# DHT11은 board.D17 핀에 연결
dht = DHT11(PIN['TEMP_HUM'], use_pulseio=False)

# 현재 온도/습도 값을 저장하는 변수
_current_temperature = None
_current_humidity = None
_status_lock = threading.Lock()  # 스레드 안전성을 위한 Lock

def read_temp_hum_status():
    """온습도 센서의 현재 값을 한 번 읽어서 반환"""
    try:
        global _current_temperature, _current_humidity
        temp = dht.temperature
        hum = dht.humidity
  
        with _status_lock:
            if temp is not None and hum is not None:
                _current_temperature = temp
                _current_humidity = hum
                # print(f'Temperature : {temp:.1f}C, Humidity : {hum:.1f}%') # 너무 자주 출력될 수 있으므로 주석 처리
                return temp, hum
            else:
                print('Failed to retrieve DHT11 data.')
                _current_temperature = None
                _current_humidity = None
                return None, None
        
    except RuntimeError as err: # DHT 센서 특유의 오류 (일시적)
        print(f'DHT Sensor RuntimeError: {err}')
        with _status_lock:
            _current_temperature = None
            _current_humidity = None
        return None, None
    except Exception as err:
        print(f'Error reading DHT sensor: {err}')
        with _status_lock:
            _current_temperature = None
            _current_humidity = None
        return None, None
    
def get_current_temp_hum_status():
    """외부에서 현재 온도와 습도 값을 가져오는 함수 (스레드 안전)"""
    with _status_lock:
        return _current_temperature, _current_humidity

def monitor_temp_hum_sensor():
    """온습도 센서를 무한 루프하며 지속적으로 모니터링하는 스레드 대상 함수"""
    print("Temperature/Humidity sensor monitoring started...")
    error_count = 0
    max_errors = 5
    
    while is_system_active():
        try:
            read_temp_hum_status() # 주기적으로 온습도 상태 읽기
            error_count = 0  # 성공 시 에러 카운터 리셋
            sleep(5) # 5초마다 체크 (DHT11은 너무 자주 읽으면 오류 발생 가능)
        except Exception as e:
            error_count += 1
            print(f"Temp/Hum Monitoring Error ({error_count}/{max_errors}): {e}")
            
            if error_count >= max_errors:
                print("Temp/Hum sensor disabled due to repeated errors.")
                break  # 심각한 오류 시 해당 모듈만 비활성화
            
            sleep(10) # 오류 발생 시 잠시 대기 후 재시도 (DHT11 오류 방지)
    print("Temperature/Humidity sensor monitoring stopped.")

def cleanup():
    """리소스 정리 함수"""
    global dht
    try:
        if dht:
            dht.exit()
        print("Temp/Hum module cleaned up.")
    except Exception as e:
        print(f"Temp/Hum module cleanup error: {e}")
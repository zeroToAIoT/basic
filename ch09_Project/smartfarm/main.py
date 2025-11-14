# file: main.py
# SmartFarm Main System

import threading
from signal import pause
from time import sleep
from datetime import datetime
import os

# --- 1. 기능 모듈 임포트 ---
from lcd import update_lcd_display, lcd_cleanup
from supplyWaterMoisture import control_water_pump_auto, pump_on, pump_off, get_pump_manual_mode, water_pump_cleanup
from supplyWaterTank import control_water_tank_auto, tank_open, tank_close, get_tank_manual_mode, water_tank_cleanup
from fan import control_fan_auto, fan_on, fan_off, get_fan_manual_mode, fan_cleanup
from rgbled import update_rgbled, set_color, rgbled_cleanup
from buzzer import check_and_alert, buzzer_cleanup

# 루프형 모듈들 (루프 함수 및 cleanup 임포트)
from music import music_loop, start_music_manual, stop_music_manual, music_cleanup
# 👈 수정: plantGrowth에서 analyze_growth_stage_latest 대신 growth_analysis_loop만 임포트
from plantGrowth import growth_analysis_loop
from camera import capture_image_loop
# (camera.py는 stop_event로 자체 cleanup 하므로 cleanup 함수 임포트 안 함)

# 입력 모듈들
from bluedot import set_bluedot, start_bluedot_service, bluedot_cleanup
from button import btn, set_button, button_cleanup

# "Dumb" 센서 모듈들 (값 읽기 함수 및 cleanup 임포트)
from temp_hum import read_temp_hum, temp_hum_cleanup
from moisture import read_moisture, moisture_cleanup
from waterSensor import read_water_level, water_sensor_cleanup
from light import read_light_sensor, light_sensor_cleanup

# Config
from config import IMAGE_PATH, CAMERA_INTERVAL, DB_PATH

# --- 2. 전역 변수 및 상태 관리 ---
smartFarm_active = False
stop_event = threading.Event()
_active_threads = [] 

_system_status = {
    'temp': None, 'hum': None, 'moisture': None, 'water_level': None,
    'light_level': None, 'growth_level': None, 'growth_confidence': None,
    'system_message': "Ready to activate...",
    'manual_fan': False, 'manual_pump': False, 'manual_tank': False,
    'last_updated': None
}
_status_lock = threading.Lock() # plantGrowth.py와 상태를 공유 Lock

# --- 3. 시스템 활성화/비활성화 함수 ---
def activate():
    global smartFarm_active, _active_threads
    if smartFarm_active:
        print('[Main] SmartFarm System already activated.')
        return

    smartFarm_active = True
    stop_event.clear()
    _active_threads = []
    print('\n--- SmartFarm System Activated ---')
    _system_status['system_message'] = "System Activated"

    # --- 스레드 시작 ---
    # 1. 중앙 제어 허브 스레드 (모든 센서 읽기 + 자동 제어 + LCD 업데이트)
    hub_thread = threading.Thread(target=_main_monitoring_and_control_loop, args=(stop_event,), daemon=True)
    hub_thread.start()
    _active_threads.append(hub_thread)

    # 2. 카메라 캡처 스레드
    camera_thread = threading.Thread(target=capture_image_loop,
                                     args=(stop_event, IMAGE_PATH, CAMERA_INTERVAL),
                                     daemon=True)
    camera_thread.start()
    _active_threads.append(camera_thread)

    # 3. AI 분석 및 DB 저장 스레드
    analysis_thread = threading.Thread(target=growth_analysis_loop,
                                       args=(stop_event, CAMERA_INTERVAL, _status_lock, _system_status),
                                       daemon=True)
    analysis_thread.start()
    _active_threads.append(analysis_thread)
    
    # 4. 자동 음악 재생 스레드
    music_thread = threading.Thread(target=music_loop,
                                    args=(stop_event, get_system_status),
                                    daemon=True)
    music_thread.start()
    _active_threads.append(music_thread)

    # 5. BlueDot 서비스 스레드
    bluedot_thread = threading.Thread(target=start_bluedot_service, daemon=True)
    bluedot_thread.start()
    _active_threads.append(bluedot_thread)
    
    print('[Main] All monitoring and control threads started.')

def deactivate():
    global smartFarm_active
    if not smartFarm_active:
        print('[Main] SmartFarm System already deactivated.')
        return
    
    smartFarm_active = False
    stop_event.set()
    print('[Main] --- SmartFarm System Deactivated ---')
    _system_status['system_message'] = "System Deactivated"
    print('[Main] Deactivation signal sent to all threads.')

def get_system_status():
    return smartFarm_active and not stop_event.is_set()

# --- 4. 중앙 모니터링 및 제어 루프 (Hub Thread) ---
def _main_monitoring_and_control_loop(stop_event):
    print("[Main Hub] Monitoring and control loop started...")
    last_dht_read_time = datetime.now()
    
    while not stop_event.is_set():
        current_time = datetime.now()
        
        # --- 4.1. 센서 값 읽기 (중앙 허브에서만) ---
        with _status_lock:
            # DHT11 (2초 이상 간격으로만 읽기)
            if (current_time - last_dht_read_time).total_seconds() >= 2.0:
                _system_status['temp'], _system_status['hum'] = read_temp_hum()
                last_dht_read_time = current_time
            
            _system_status['moisture'] = read_moisture()
            _system_status['water_level'] = read_water_level()
            _system_status['light_level'] = read_light_sensor()
            
            _system_status['last_updated'] = current_time.strftime('%H:%M:%S')

            # --- 4.2. 액추에이터 자동 제어 (수동 모드 확인) ---
            _system_status['manual_fan'] = get_fan_manual_mode()
            _system_status['manual_pump'] = get_pump_manual_mode()
            _system_status['manual_tank'] = get_tank_manual_mode()

            # 자동 제어 함수 호출
            control_fan_auto(_system_status['temp'], _system_status['hum'], _system_status['manual_fan'])
            control_water_pump_auto(_system_status['moisture'], _system_status['manual_pump'])
            control_water_tank_auto(_system_status['water_level'], _system_status['manual_tank'])
            
            # LED 및 부저 제어 (수동 모드가 아닐 때만)
            update_rgbled(_system_status['light_level'], 
                          _system_status['growth_level'], 
                          _system_status['growth_confidence'])
            check_and_alert(_system_status['temp'], _system_status['hum'],
                            _system_status['moisture'], _system_status['water_level'])

            # --- 4.3. LCD 업데이트 ---
            update_lcd_display(_system_status) 

        sleep(0.1) 
    print("[Main Hub] Monitoring and control loop stopped.")

# --- 5. 메인 함수 ---
def main():
    # 1. 경로 생성
    os.makedirs(IMAGE_PATH, exist_ok=True)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # 2. 버튼 및 BlueDot에 메인 제어 함수 연결
    set_button(activate, deactivate, get_system_status)
    set_bluedot(
        activate, deactivate,
        fan_on, fan_off,
        pump_on, pump_off,
        tank_open, tank_close,
        lambda: set_color('white'),
        lambda: set_color('red'),
        lambda: set_color('blue'),
        lambda: set_color('off'),
        start_music_manual,
        stop_music_manual
    )
    
    print('[Main] SmartFarm Main Controller Initialized.')
    print('[Main] Waiting for button press or BlueDot to activate...')
    
    # activate() # 👈 자동 시작을 원하면 주석 해제 (디버깅 시 유용)
  
    try:
        pause() # 물리 버튼(btn.when_pressed) 이벤트를 기다림
    except KeyboardInterrupt:
        print('\n[Main] SmartFarm system stopped by user (Ctrl+C).')
    except Exception as e:
        print(f'[Main] An unexpected error occurred: {e}')
    finally:
        print('[Main] --- Cleaning up SmartFarm resources ---')
        deactivate()
        
        lcd_cleanup()
        rgbled_cleanup()
        buzzer_cleanup()
        temp_hum_cleanup()
        moisture_cleanup()
        water_sensor_cleanup()
        light_sensor_cleanup()
        water_pump_cleanup() 
        water_tank_cleanup() 
        music_cleanup()
        bluedot_cleanup()
        button_cleanup()
        fan_cleanup()

        print('[Main] All SmartFarm resources cleaned up.')
        print('[Main] SmartFarm system finished.')

if __name__ == '__main__':
    main()
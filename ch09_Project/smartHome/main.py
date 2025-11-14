# file: main.py
# SmartHome Main Controller (Updated with Threading, State Management, and Cleanup)

import threading
from signal import pause
from time import sleep
from datetime import datetime

# --- 1. 기능 모듈 임포트 ---
# 센서 모니터링을 위한 모듈 (이제 monitor_ 함수를 스레드 대상으로 사용)
from pir_module import monitor_pir_sensors, get_current_motion_status, cleanup as pir_cleanup
from fire_module import monitor_fire_sensor, get_current_fire_status, cleanup as fire_cleanup
from light_module import monitor_light_sensor, get_current_light_value, cleanup as light_cleanup
from temp_hum_module import monitor_temp_hum_sensor, get_current_temp_hum_status, cleanup as dht_cleanup

# 디스플레이 모듈 (상태를 전달받아 표시)
from lcd_module import update_display, cleanup as lcd_cleanup
from multiFnd_module import multiFnd_display_time, cleanup as fnd_cleanup # FND는 내부 무한루프

# 알람 및 기타 기능
from morningCall_module import morningCall_play, cleanup as mc_cleanup
from buzzer_module import control_by_fire as buzzer_control_by_fire, control_by_pir as buzzer_control_by_pir, cleanup as buzzer_cleanup 
from led_module import control_by_light, control_by_fire, control_by_pir, cleanup as led_cleanup 

# 시스템 활성/비활성 제어 모듈
from button_module import btn, toggle_system, set_control_functions as set_button_functions, cleanup as button_cleanup
from bluedot_module import bd, set_control_functions as set_bluedot_functions, cleanup as bluedot_cleanup 


# --- 2. 시스템 전역 상태 변수 ---
from system_status import set_system_active, is_system_active
smartHome_active = False  # 하위 호환성을 위해 유지 
_active_threads = []     
_system_status = {       
    'fire_alert': False,
    'pir_location': None,
    'temp': None,
    'hum': None,
    'light_level': None,
    'last_updated': None,
    'system_message': "Ready to activate..."
}
_status_lock = threading.Lock() 

# --- 3. 시스템 활성화/비활성화 함수 ---
def activate():
    global smartHome_active, _active_threads
    if smartHome_active:
        print('SmartHome System already activated')
        return

    smartHome_active = True
    set_system_active(True)  # 공유 상태 모듈에 알림
    print('\n--- SmartHome System Activated ---')
    _system_status['system_message'] = "System Activated"
    
    # 3.1. 각 기능 모듈의 모니터링 스레드 시작
    # FND (시간 표시)
    fnd_thread = threading.Thread(target=multiFnd_display_time, daemon=True)
    fnd_thread.start()
    _active_threads.append(fnd_thread)
    
    # 온습도 센서 모니터링
    dht_thread = threading.Thread(target=monitor_temp_hum_sensor, daemon=True)
    dht_thread.start()
    _active_threads.append(dht_thread)

    # PIR 센서 모니터링 (움직임 감지)
    pir_thread = threading.Thread(target=monitor_pir_sensors, daemon=True)
    pir_thread.start()
    _active_threads.append(pir_thread)

    # 화재 센서 모니터링
    fire_thread = threading.Thread(target=monitor_fire_sensor, daemon=True)
    fire_thread.start()
    _active_threads.append(fire_thread)

    # 조도 센서 모니터링 (LED 자동 제어를 위해 필요)
    light_thread = threading.Thread(target=monitor_light_sensor, daemon=True)
    light_thread.start()
    _active_threads.append(light_thread)
    
    # 모닝콜 기능 (설정된 시간에 재생)
    mc_thread = threading.Thread(target=morningCall_play, daemon=True)
    mc_thread.start()
    _active_threads.append(mc_thread)

    # --- 3.2. 메인 상태 업데이트 및 LCD/LED/Buzzer 제어 스레드 시작 ---
    status_update_thread = threading.Thread(target=_monitor_and_control_loop, daemon=True)
    status_update_thread.start()
    _active_threads.append(status_update_thread)

    bluedot_thread = threading.Thread(target=_start_bluedot_service, daemon=True)
    bluedot_thread.start()
    _active_threads.append(bluedot_thread)


def deactivate():
    global smartHome_active, _active_threads
    if not smartHome_active:
        print('SmartHome System already deactivated')
        return

    smartHome_active = False
    set_system_active(False)  # 공유 상태 모듈에 알림
    print('--- SmartHome System Deactivated ---')
    _system_status['system_message'] = "System Deactivated"

    led_cleanup()
    buzzer_cleanup()
    lcd_cleanup()
    mc_cleanup() 

def get_system_status():
    return smartHome_active

# --- 4. BlueDot 서비스 시작 함수 (bluedot_module.py의 pause()를 포함) ---
def _start_bluedot_service():
    print("BlueDot service started, waiting for button presses...")
    try:
        pause() # BlueDot 이벤트를 계속 대기
    except KeyboardInterrupt:
        print("BlueDot service stopped.")
    except Exception as err:
        print(f"Error in BlueDot service: {err}")
    finally:
        bluedot_cleanup() # BlueDot 리소스 정리


# --- 5. 메인 모니터링 및 제어 루프 스레드 ---
def _monitor_and_control_loop():
    print("Main monitoring and control loop started...")
    while smartHome_active: 
        with _status_lock: 
            _system_status['fire_alert'] = get_current_fire_status()
            _system_status['pir_location'] = get_current_motion_status()
            _system_status['temp'], _system_status['hum'] = get_current_temp_hum_status()
            _system_status['light_level'] = get_current_light_value()
            _system_status['last_updated'] = datetime.now().strftime('%H:%M:%S')

            update_display(_system_status)

            # 우선순위: 화재 > PIR > 조도
            # 화재 감지 시 최우선 처리
            if _system_status['fire_alert']:
                control_by_fire(True)
                buzzer_control_by_fire(True)
            # PIR 감지 시 (화재가 아닐 때만)
            elif _system_status['pir_location']:
                control_by_pir(True)
                buzzer_control_by_pir(True)
            # 정상 상태: 조도에 따라 LED 제어
            else:
                control_by_light(_system_status['light_level'])
                # 화재/PIR 알람이 해제되었을 때 명시적으로 끄기
                control_by_fire(False)
                buzzer_control_by_fire(False) 


        sleep(1.5) 
    print("Main monitoring and control loop stopped.")


# --- 6. 메인 함수 ---
def main():
    # 6.1. 버튼 및 블루닷 모듈에 시스템 제어 함수들 전달
    set_button_functions(activate, deactivate, get_system_status)
    set_bluedot_functions(activate, deactivate)
    
    # 6.2. 블루닷 및 물리 버튼 눌림 대기 (이벤트 기반)
    print('SmartHome Main Controller Initialized.')
    print('Waiting for BlueDot button & physical button press to activate/deactivate...')
    
    try:
        pause() 

    except KeyboardInterrupt:
        print('\nSmartHome system stopped by user (Ctrl+C).')
    except Exception as err:
        print(f'An unexpected error occurred in main: {err}')
    finally:
        print('--- Cleaning up SmartHome resources ---')
        deactivate() 

        pir_cleanup()
        fire_cleanup()
        light_cleanup()
        dht_cleanup()
        lcd_cleanup()
        fnd_cleanup()
        mc_cleanup()
        buzzer_cleanup()
        led_cleanup()
        button_cleanup()

        print('All SmartHome resources cleaned up.')
        print('SmartHome system finished.')

if __name__ == '__main__':
    main()
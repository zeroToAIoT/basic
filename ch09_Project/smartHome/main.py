# file: main.py
# SmartHome Main Controller

import threading
from signal import pause

from pir_module import read_pir_value
from fire_module import fire_detect
from lcd_module  import lcd_display
from morningCall_module import morningCall_play
from multiFnd_module import multiFnd_display_time
from button_module import btn, toggle_system, set_control_functions as set_button_functions
from bluedot_module import bluedot_module, set_control_functions as set_bluedot_functions

# SmartHome Main Controller
smartHome_active = False

def activate():
    global smartHome_active
    if smartHome_active:
        print('SmartHome System already activated')
        return

    smartHome_active = True
    print('SmartHome System Activated')

    threading.Thread(target=multiFnd_display_time, args=(12, 0), daemon=True).start()
    threading.Thread(target=lcd_display, daemon=True).start()
    threading.Thread(target=read_pir_value, daemon=True).start()
    threading.Thread(target=fire_detect, daemon=True).start()
    threading.Thread(target=morningCall_play, daemon=True).start()
    threading.Thread(target=bluedot_module, daemon=True).start()

def deactivate():
    global smartHome_active
    if not smartHome_active:
        print('SmartHome System already deactivated')
        return

    smartHome_active = False
    print('SmartHome System Deactivated')

def get_system_status():
    """시스템 상태 확인 함수"""
    return smartHome_active

def main():
    # 버튼과 블루닷 모듈에 제어 함수들 전달
    set_button_functions(activate, deactivate, get_system_status)
    set_bluedot_functions(activate, deactivate)
    
    btn.when_pressed = toggle_system  

    print('Waiting for BlueDot button & physical button press...')

    activate()

    try:
        pause()

    except KeyboardInterrupt:
        print('SmartHome system stopped.Ctrl+C')
    finally:
        print('SmartHome system finished.')

if __name__ == '__main__':
    main()
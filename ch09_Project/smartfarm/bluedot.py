# file: bluedot.py
from bluedot import BlueDot
from config import BLUEDOT_BUTTONS

# ✅ alias 사용: 자동 제어와 구분
from fan import fan_on as manual_fan_on, fan_off as manual_fan_off
from supplyWaterMoisture import pump_on as manual_pump_on, pump_off as manual_pump_off
from supplyWaterTank import tank_open as manual_tank_open, tank_close as manual_tank_close
from music import play_music as manual_play_music, stop_music as manual_stop_music
from rgbled import set_color

bd = BlueDot(cols=4, rows=4)

# Global variables for functions
activate_func = None
deactivate_func = None

def set_bluedot(activate, deactivate):
    global activate_func, deactivate_func
    activate_func = activate
    deactivate_func = deactivate

# 버튼-액션 매핑 딕셔너리 (좌표 기반)
ACTIONS = {
    BLUEDOT_BUTTONS['activate']:   lambda: activate_func() if activate_func else None,
    BLUEDOT_BUTTONS['deactivate']: lambda: deactivate_func() if deactivate_func else None,
    BLUEDOT_BUTTONS['fan_on']:     manual_fan_on,
    BLUEDOT_BUTTONS['fan_off']:    manual_fan_off,
    BLUEDOT_BUTTONS['water_pump_on']:  manual_pump_on,
    BLUEDOT_BUTTONS['water_pump_off']: manual_pump_off,
    BLUEDOT_BUTTONS['waterTank_servo_on']:  manual_tank_open,
    BLUEDOT_BUTTONS['waterTank_servo_off']: manual_tank_close,
    BLUEDOT_BUTTONS['rgb_white']:  lambda: set_color('white'),
    BLUEDOT_BUTTONS['rgb_red']:    lambda: set_color('red'),
    BLUEDOT_BUTTONS['rgb_blue']:   lambda: set_color('blue'),
    BLUEDOT_BUTTONS['rgb_off']:    lambda: set_color('off'),
    BLUEDOT_BUTTONS['music_play']: manual_play_music,
    BLUEDOT_BUTTONS['music_stop']: manual_stop_music,
}

def start_bluedot(pos):
    try:
        key = (pos.col, pos.row)
        action = ACTIONS.get(key)
        if action:
            print(f'Executing action for {key}')
            action()
        else:
            print(f'No action mapped for {key}')
    except Exception as err:
        print(f'Error: {err}')

bd.when_pressed = start_bluedot
print('BlueDot is active! Press buttons to control the Smart Farm.')
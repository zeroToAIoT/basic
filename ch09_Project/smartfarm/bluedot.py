# file: bluedot.py
from bluedot import BlueDot
from config import BLUEDOT_BUTTONS

from fan import fan_on as manual_fan_on, fan_off as manual_fan_off
from supplyWaterMoisture import pump_on as manual_pump_on, pump_off as manual_pump_off
from supplyWaterTank import tank_open as manual_tank_open, tank_close as manual_tank_close
from music import start_music_manual, stop_music_manual
from rgbled import set_color

bd = BlueDot(cols=4, rows=4)

# Global variables for functions (main.py에서 주입받을 activate/deactivate)
activate_func = None
deactivate_func = None

def set_bluedot(activate, deactivate,
                fan_on_cb, fan_off_cb,
                pump_on_cb, pump_off_cb,
                tank_open_cb, tank_close_cb,
                rgb_white_cb, rgb_red_cb, rgb_blue_cb, rgb_off_cb,
                music_play_cb, music_stop_cb): 
    global activate_func, deactivate_func
    activate_func = activate
    deactivate_func = deactivate

    # ACTIONS 딕셔너리를 초기화하거나 업데이트
    ACTIONS[BLUEDOT_BUTTONS['fan_on']] = fan_on_cb
    ACTIONS[BLUEDOT_BUTTONS['fan_off']] = fan_off_cb
    ACTIONS[BLUEDOT_BUTTONS['water_pump_on']] = pump_on_cb
    ACTIONS[BLUEDOT_BUTTONS['water_pump_off']] = pump_off_cb
    ACTIONS[BLUEDOT_BUTTONS['waterTank_servo_on']] = tank_open_cb
    ACTIONS[BLUEDOT_BUTTONS['waterTank_servo_off']] = tank_close_cb
    ACTIONS[BLUEDOT_BUTTONS['rgb_white']] = rgb_white_cb
    ACTIONS[BLUEDOT_BUTTONS['rgb_red']] = rgb_red_cb
    ACTIONS[BLUEDOT_BUTTONS['rgb_blue']] = rgb_blue_cb
    ACTIONS[BLUEDOT_BUTTONS['rgb_off']] = rgb_off_cb
    ACTIONS[BLUEDOT_BUTTONS['music_play']] = music_play_cb
    ACTIONS[BLUEDOT_BUTTONS['music_stop']] = music_stop_cb


ACTIONS = {
    BLUEDOT_BUTTONS['activate']:   lambda: activate_func() if activate_func else print("[BlueDot] Activate func not set"),
    BLUEDOT_BUTTONS['deactivate']: lambda: deactivate_func() if deactivate_func else print("[BlueDot] Deactivate func not set"),
}

def on_bluedot_pressed(pos):
    try:
        key = (pos.col, pos.row)
        action = ACTIONS.get(key)
        if action:
            print(f'[BlueDot] Executing action for {key}')
            action()
        else:
            print(f'[BlueDot] No action mapped for {key}')
    except Exception as err:
        print(f'[BlueDot Error] on_bluedot_pressed: {err}')

# BlueDot의 when_pressed 이벤트에 콜백 함수 연결
bd.when_pressed = on_bluedot_pressed

def start_bluedot_service():
    print('[BlueDot] Service is active! Ready to receive presses.')

def bluedot_cleanup():
    bd.stop()
    print("[BlueDot] BlueDot resources released.")

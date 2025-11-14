# file: bluedot_module.py
# Smart Home System with BlueDot Buttons (Updated)

from bluedot import BlueDot
# from signal import pause # 이제 main.py의 _start_bluedot_service에서 pause()를 호출함

bd = BlueDot(cols=2, rows=1)

# Global variables for functions (main.py에서 activate/deactivate 함수를 받기 위함)
activate_func = None
deactivate_func = None
  
def set_control_functions(activate, deactivate):
    """main.py의 activate/deactivate 함수를 BlueDot 콜백에 연결"""
    global activate_func, deactivate_func
    activate_func = activate
    deactivate_func = deactivate
  
def _on_activate_button_pressed(): # BlueDot 버튼 콜백 함수
    global activate_func
    if activate_func:
        activate_func()
  
def _on_deactivate_button_pressed(): # BlueDot 버튼 콜백 함수
    global deactivate_func
    if deactivate_func:
        deactivate_func()
  
# setting bd[0,0] button (Activate)
bd[0, 0].color = 'green'
bd[0, 0].size = (100, 100)
bd[0, 0].label = 'Activate SmartHome System'
bd[0, 0].when_pressed = _on_activate_button_pressed # 콜백 함수 연결
  
# setting bd[0,1] button (Deactivate)
bd[0, 1].color = 'red'
bd[0, 1].size = (100, 100)
bd[0, 1].label = 'Deactivate SmartHome System'
bd[0, 1].when_pressed = _on_deactivate_button_pressed # 콜백 함수 연결
  
print('BlueDot module initialized. Waiting for main controller to start service...')

def cleanup():
    """리소스 정리 함수"""
    global bd
    try:
        if bd:
            bd.close()
        print("BlueDot module cleaned up.")
    except Exception as e:
        print(f"BlueDot module cleanup error: {e}")


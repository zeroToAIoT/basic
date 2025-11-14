# file: button_module.py
# Button Control Module for Smart Home System

from gpiozero import Button
from config import PIN

btn = Button(PIN["BUTTON"])

# Global variables for functions
activate_func = None
deactivate_func = None
system_status_func = None

def set_control_functions(activate, deactivate, get_status=None):
    global activate_func, deactivate_func, system_status_func
    activate_func = activate
    deactivate_func = deactivate
    system_status_func = get_status

def toggle_system():
    global activate_func, deactivate_func, system_status_func
    
    if activate_func and deactivate_func:
        if system_status_func:
            if system_status_func():
                print("Button pressed - deactivating system")
                deactivate_func()
            else:
                print("Button pressed - activating system")
                activate_func()
        else:
            print("Button pressed - activating system")
            activate_func()

btn.when_pressed = toggle_system

def cleanup():
    """리소스 정리 함수"""
    global btn
    try:
        if btn:
            btn.close()
        print("Button module cleaned up.")
    except Exception as e:
        print(f"Button module cleanup error: {e}")
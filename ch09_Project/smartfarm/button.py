# file: button.py
# Button Control for SmartFarm System

from gpiozero import Button

from config import PIN

btn = Button(PIN['BUTTON'], bounce_time=0.1)

# Global variables to store functions
activate_func = None
deactivate_func = None
system_status_func = None

def set_button(activate, deactivate, get_status=None):
    global activate_func, deactivate_func, system_status_func
    activate_func = activate
    deactivate_func = deactivate
    system_status_func = get_status

def toggle_system():
    global activate_func, deactivate_func, system_status_func
    
    if activate_func and deactivate_func:
        if system_status_func:
            if system_status_func():
                print('Button pressed - deactivating SmartFarm system')
                deactivate_func()
            else:
                print('Button pressed - activating SmartFarm system')
                activate_func()
        else:
            print('Button pressed - activating SmartFarm system')
            activate_func()

def button_cleanup():
    btn.close()

btn.when_pressed = toggle_system

# file: bluedot_module.py

# Smart Home System with BlueDot Buttons

from bluedot import BlueDot
from signal import pause

bd = BlueDot(cols=2, rows=1)

# Global variables for functions
activate_func = None
deactivate_func = None

def set_control_functions(activate, deactivate):
    global activate_func, deactivate_func
    activate_func = activate
    deactivate_func = deactivate

def activate_system():
    global activate_func
    if activate_func:
        activate_func()

def deactivate_system():
    global deactivate_func
    if deactivate_func:
        deactivate_func()

# setting bd[0,0] button
bd[0, 0].color = 'green'
bd[0, 0].size = (100, 100)
bd[0, 0].label = 'Activate SmartHome System'
bd[0, 0].when_pressed = activate_system

# setting bd[0,1] button
bd[0, 1].color = 'red'
bd[0, 1].size = (100, 100)
bd[0, 1].label = 'Deactivate SmartHome System'
bd[0, 1].when_pressed = deactivate_system

print('Waiting for BlueDot button press...')

pause()
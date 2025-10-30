# file: pir_module.py
# PIR Sensor Module (Event-Driven)

from gpiozero import MotionSensor
from config import PIN
from camera_module import capture_image

pir_door = MotionSensor(PIN['PIR_DOOR'])
pir_window = MotionSensor(PIN['PIR_WINDOW'])

def read_pir_value():

    if pir_door.motion_detected:
        print('Motion detected at door')
        print('Capturing image...')
        capture_image('door')
        return 'door'

    elif pir_window.motion_detected:
        print('Motion detected at window')
        print('Capturing image...')
        capture_image('window')
        return 'window'

    else:
        print('No motion detected')
        return None
# file: button_module_advanced.py
# Button Control Module for Smart Home System

from gpiozero.pins.pigpio import PiGPIOFactory
from config import REMOTE_PI_IP, PIN
import logging

from gpiozero import Button
from main import activate, deactivate

# Remote Raspberry Pi IP
remotePi = PiGPIOFactory(host=REMOTE_PI_IP)

btn = Button(PIN['BUTTON'], pin_factory=remotePi, bounce_time=0.1)

# Record
logging.basicConfig(filename='button.log', level=logging.INFO, format='%(asctime)s - %(message)s')

smartHome_active = False

def toggle_system():
    global smartHome_active

    if smartHome_active:
        logging.info('Deactivating Smart Home System')
        print('Deactivating Smart Home System')
        deactivate()
    else:
        logging.info('Activating Smart Home System')
        print('Activating Smart Home System')
        activate()
    
    smartHome_active = not smartHome_active

btn.when_pressed = toggle_system
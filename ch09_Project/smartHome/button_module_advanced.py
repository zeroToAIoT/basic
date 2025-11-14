# file: button_module_advanced.py
# Button Control Module for Smart Home System (Remote GPIO)
# 
# 주의: 이 모듈은 원격 Raspberry Pi의 GPIO를 제어하기 위한 고급 버전입니다.
# 순환 import를 방지하기 위해 콜백 패턴을 사용합니다.
# main.py에서 set_control_functions()를 호출하여 activate/deactivate 함수를 전달해야 합니다.

from gpiozero.pins.pigpio import PiGPIOFactory
from config import REMOTE_PI_IP, PIN
import logging
import os

from gpiozero import Button

# Remote Raspberry Pi IP
remotePi = PiGPIOFactory(host=REMOTE_PI_IP)

btn = Button(PIN['BUTTON'], pin_factory=remotePi, bounce_time=0.1)

# Record
log_file = os.path.join(os.path.dirname(__file__), 'logs', 'button.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Global variables for functions (순환 import 방지를 위해 콜백 패턴 사용)
activate_func = None
deactivate_func = None
system_status_func = None

def set_control_functions(activate, deactivate, get_status=None):
    """main.py의 activate/deactivate 함수를 버튼 콜백에 연결 (순환 import 방지)"""
    global activate_func, deactivate_func, system_status_func
    activate_func = activate
    deactivate_func = deactivate
    system_status_func = get_status

def toggle_system():
    """버튼이 눌렸을 때 호출되는 콜백 함수"""
    global activate_func, deactivate_func, system_status_func
    
    if activate_func and deactivate_func:
        if system_status_func:
            if system_status_func():
                logging.info('Deactivating Smart Home System')
                print('Deactivating Smart Home System')
                deactivate_func()
            else:
                logging.info('Activating Smart Home System')
                print('Activating Smart Home System')
                activate_func()
        else:
            logging.info('Activating Smart Home System')
            print('Activating Smart Home System')
            activate_func()

btn.when_pressed = toggle_system

def cleanup():
    """리소스 정리 함수"""
    global btn, remotePi
    try:
        if btn:
            btn.close()
        if remotePi:
            remotePi.close()
        print("Button module (advanced) cleaned up.")
    except Exception as e:
        print(f"Button module (advanced) cleanup error: {e}")
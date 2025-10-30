# file: buzzer_module.py
# Buzzer Control Module for Smart Home System

from gpiozero import Buzzer
from config import PIN

buzzer = Buzzer(PIN['BUZZER'])

def by_fire(fire_detected):
    try:
        if fire_detected:
            print('Fire detected! Buzzer Alarm.')
            buzzer.beep(on_time=0.2, off_time=0.2, n=None)
        else:
            print('No fire detected. Stopping Buzzer.')
            buzzer.off()

    except Exception as err:
        print(f'Buzzer Control Error: {err}')

def by_pir(pir_detected):
    try:
        if pir_detected:
            print('Motion detected! Buzzer on.')
            buzzer.beep(on_time=0.5, off_time=0.5, n=5)
        else:
            print('Nothing.. Stopping Buzzer.')
            buzzer.off()

    except Exception as e:
        print(f'Buzzer Control Error: {e}')
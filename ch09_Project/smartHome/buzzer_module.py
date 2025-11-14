# file: buzzer_module.py
# Buzzer Control Module for Smart Home System (Dumb Module)

from gpiozero import Buzzer
from config import PIN

buzzer = Buzzer(PIN['BUZZER'])

# 부저를 켜거나 끄는 기본 함수
def turn_on():
    buzzer.on()
    print("Buzzer ON.")

def turn_off():
    buzzer.off()
    print("Buzzer OFF.")

# 부저를 반복해서 울리는 기본 함수
def beep_buzzer(on_time, off_time, n=None):
    buzzer.beep(on_time=on_time, off_time=off_time, n=n)
    print(f"Buzzer beeping ({on_time}/{off_time}).")

def control_by_fire(fire_detected): # 외부에서 fire_detected 값을 인자로 받음
    try:
        if fire_detected:
            print('Fire detected! Buzzer Alarm (beep).')
            buzzer.beep(on_time=0.2, off_time=0.2, n=None) # n=None은 무한 반복
        else:
            print('No fire detected. Stopping Buzzer.')
            buzzer.off()
    except Exception as err:
        print(f'Buzzer Control Error: {err}')
        buzzer.off()

def control_by_pir(pir_detected):
    try:
        if pir_detected:
            print('Motion detected! Buzzer on (5 beeps).')
            buzzer.beep(on_time=0.5, off_time=0.5, n=5)
        else:
            print('No motion. Stopping Buzzer.')
            buzzer.off()
    except Exception as e:
        print(f'Buzzer Control Error: {e}')
        buzzer.off()

def cleanup():
    buzzer.off()
    buzzer.close()
    print('Buzzer module cleaned up.')